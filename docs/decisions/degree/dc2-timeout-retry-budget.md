---
title: "DC-2 タイムアウト・リトライ・予算（コスト上限）"
description: "エージェントのタイムアウト・リトライ回数・セッションコスト上限を決める連続量パラメータ。"
status: done
---

# DC-2 タイムアウト・リトライ・予算（コスト上限）

## 概要

エージェントは従来の API に比べて桁違いに遅く、1セッションで数百円のトークンコストがかかることもあります。タイムアウトが短すぎれば正当な処理が途中で打ち切られ、長すぎれば無限ループで高額請求が発生します。「何秒待つか」「何回リトライするか」「1セッションいくらまで使ってよいか」——この3つの上限をどう決めるかが本項のテーマです。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-2
parameter: timeout_retry_budget
rules:
  - condition: "operation_type == 'simple_qa' AND expected_duration_seconds <= 10"
    timeout_ttft_seconds: 5
    timeout_total_seconds: 30
    max_retries: 2
    session_budget_multiplier: 1.5
    reason: "短時間Q&AはTTFT・全体タイムアウトを短く設定し、リトライを2回に制限して過剰コストを防ぐ"
  - condition: "operation_type == 'document_analysis' OR expected_duration_seconds > 30"
    timeout_ttft_seconds: 15
    timeout_total_seconds: 300
    max_retries: 2
    session_budget_multiplier: 3.0
    reason: "長文分析は全体タイムアウトを延ばす。300秒を常に超える場合は非同期化（RT-8）を検討する"
  - condition: "operation_type == 'multi_step_workflow' AND steps_include_human_approval == true"
    timeout_ttft_seconds: 15
    timeout_total_seconds: null
    max_retries: 2
    session_budget_multiplier: 5.0
    reason: "人間の承認待ちステップがある場合は全体タイムアウト設定を外し、永続ワークフロー（RT-8）でステップ別予算上限を設ける"
  - condition: "idempotency == 'non_idempotent' AND operation_type IN ['write', 'send', 'publish']"
    max_retries: 0
    reason: "非冪等な操作（書き込み・送信）のリトライは二重実行の害が大きい。リトライ対象は冪等なステップのみに限定する"
  - condition: "operation_type == 'multi_agent'"
    session_budget_multiplier: "N * single_agent_budget"
    reason: "マルチエージェント構成では推論コストがN倍になるため、GV-8の部門別予算と連動させ予算上限を厳格にする"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（厳しすぎ） | タイムアウトが短すぎ、リトライ不可、予算が少なすぎ | 正当な処理が途中で打ち切られ、タスク完了率が低下します |
| 過大（緩すぎ） | タイムアウトが長すぎ、無制限リトライ、予算上限なし | 無限ループ・暴走による高額請求やリソース占有が発生します |

## 判断基準

- **タイムアウト**：TTFT（Time to First Token）と全体タイムアウト（無進捗時間）は別に設定します。TTFT はモデルが応答を開始しているかの確認に用い、全体タイムアウトは処理が前に進んでいるかの判定に使います。
- **リトライ**：冪等なステップだけをリトライ対象にします。指数バックオフ＋ジッタで最大2〜3回に制限します。書き込みや送信といった非冪等な操作は、リトライで二重実行が起きるため対象から外します。
- **セッション予算**：コスト（トークン消費額）と時間（経過時間）の両面で上限を設けます。各ステップの予算はセッション全体の予算に従属させます。
- **マルチエージェント構成**：[RT-2 RACI-based Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md) では推論コストが N 倍になります。予算上限を特に厳格に設定し、部門別予算とも連動させます。

## 調整の仕組み

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でセッション単位のコスト・所要時間・リトライ回数・タイムアウト発生率を計測します。
- [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) の部門別予算と連動させ、予算超過時の挙動（停止・縮退・承認昇格）をあらかじめ定義しておきます。
- タイムアウト率が高い処理はタスク分割や非同期化（[RT-8](../../patterns/rt-runtime/rt8-durable-workflow.md)）を検討します。

## 関連パターン

- [RT-2 RACI-based Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md) — マルチエージェントでのコスト増加
- [RT-8 Durable Workflow](../../patterns/rt-runtime/rt8-durable-workflow.md) — タイムアウトを超える長時間処理の対策
- [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) — 予算管理・配賦の仕組み
- [GV-9 Incident Response & Kill Switch](../../patterns/gv-governance/gv9-incident-response-kill-switch.md) — 暴走時の強制停止

## 候補と推奨

| 状況／前提 | 推奨設定 | 必要パターン | トレードオフ |
|---|---|---|---|
| 対話型Copilot | 短タイムアウト（30秒）・低リトライ | EX-1, GV-5 | 応答速度優先 |
| バッチ処理・レポート生成 | 長タイムアウト（5分）・リトライ3回 | RT-8, RT-9 | コスト増 |
| 全社横断分析 | 予算上限付き・段階的実行 | GV-8, RT-7 | 精度と速度のトレード |

```yaml
decision:
  id: DC-2
  title: "タイムアウト・リトライ・予算（コスト上限）"
  options:
    - id: fast
      name: "短タイムアウト・低予算"
      patterns: [EX-1, GV-5]
      pros: [応答速度, コスト抑制]
      cons: [複雑タスク未完了]
      pick_when: ["対話型", "単純Q&A"]
    - id: balanced
      name: "中間設定"
      patterns: [RT-8, GV-8]
      pros: [バランス]
      cons: [設定複雑]
      pick_when: ["複合タスク", "バッチ"]
    - id: generous
      name: "長タイムアウト・高予算"
      patterns: [RT-7, RT-8, GV-8]
      pros: [複雑タスク完了]
      cons: [コスト高, 応答遅延]
      pick_when: ["全社横断分析", "Saga"]
  default_recommendation: "対話型は30秒・バッチは5分を基準に、GV-8でコスト上限を設定"
```
