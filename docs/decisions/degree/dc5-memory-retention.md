---
title: "DC-5 メモリ保持・忘却（TTL・スコープ）"
description: "エージェントの記憶をどの程度保持し、いつ忘却するかをTTL・スコープ・ライフサイクルで決める連続量パラメータ。"
status: done
---

# DC-5 メモリ保持・忘却（TTL・スコープ）

## 概要

エージェントが「前回の会話の続き」を覚えていれば、パーソナライズが効きます。しかし退職した社員の業務記録や終了したプロジェクトの機密メモをいつまでも保持し続ければ、漏洩リスクの塊になります。「何をどのくらいの期間覚えておくか」「いつ忘れさせるか」——この設計をセッション・個人・プロジェクト・組織の各スコープ（[KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)）ごとに行う方法を示します。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-5
parameter: memory_retention_ttl
rules:
  - condition: "memory_scope == 'session'"
    ttl: session_end
    reason: "セッションスコープの記憶はセッション終了で破棄する。一時的な作業コンテキストは永続化不要"
  - condition: "memory_scope == 'personal' AND reference_frequency IN ['high', 'medium']"
    ttl: 90_days_rolling_with_extension
    reason: "頻繁に参照される個人設定・業務スタイルは90日ローリングTTLで保持し、アクセス時に延長する"
  - condition: "memory_scope == 'personal' AND reference_frequency == 'never'"
    action: auto_archive_then_delete
    ttl: 30_days_after_last_access
    reason: "未参照のメモリは自動アーカイブ・削除する。古い情報に基づく誤判断とストレージコスト増大を防ぐ"
  - condition: "lifecycle_event IN ['employee_departure', 'role_change', 'project_end']"
    action: immediate_expiry_and_permission_revocation
    reason: "プロジェクト終了・退職・異動でメモリと権限を失効させる。人事システムとの連携で自動失効を実装する"
  - condition: "permission_change_event == true"
    action: immediate_delete_all_personal_scope
    reason: "本人がメモリを削除・修正できる権利を設計に含める（ID-8 Consent & Access Transparency）"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（すぐ忘れる） | セッション終了で全消去 | 毎回同じ説明が必要になり、パーソナライズの価値が消えます |
| 過大（すべて覚える） | 全記憶を無期限保持 | 古い情報に基づく誤判断、退職者のデータ残留、ストレージコスト増大が起きます |

## 判断基準

- **重要度 × 鮮度 × 参照頻度**の3軸で残すものを選別します。古い詳細は要約に圧縮して保持するとストレージを節約できます。
- [KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) のスコープ（セッション・個人・プロジェクト・組織）ごとに TTL と失効条件を設定します。
- **ライフサイクルイベントとの連動**：プロジェクト終了・退職・異動のタイミングでメモリと権限を自動失効させる仕組みを整えます。
- **本人の消去権**：本人がメモリを削除・修正できる権利を設計に最初から組み込みます（[ID-8](../../patterns/id-identity/id8-consent-access-transparency.md)）。

## 調整の仕組み

- メモリの参照頻度・鮮度を [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) で計測し、未参照のメモリは自動アーカイブ・削除します。
- 人事システム（異動・退職イベント）と連携し、不要になったメモリを自動失効させます。
- メモリ量とタスク品質の相関を [GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) で評価し、保持ポリシーを定期的に見直します。

## 関連パターン

- [KM-4 Scoped Memory Hierarchy](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) — スコープ記憶階層の設計本体
- [ID-8 Consent & Access Transparency](../../patterns/id-identity/id8-consent-access-transparency.md) — 消去権・透明化の原則
- [RT-11 Project Digital Twin](../../patterns/rt-runtime/rt11-project-digital-twin.md) — プロジェクトスコープの記憶管理
- [TO-6 個人の記憶 vs プロジェクト/チームの記憶](../tradeoff/to6-personal-vs-team-memory.md) — 個人 vs 共有の判断軸

## 候補と推奨

| 状況／前提 | 推奨設定 | 必要パターン | トレードオフ |
|---|---|---|---|
| 一時的な作業支援 | セッション終了時に全消去 | KM-4 | パーソナライズ不可 |
| 継続的なアシスタント利用 | 90日ローリングTTL・参照時延長 | KM-4, ID-8 | ストレージコスト中・鮮度管理必要 |
| 高機密プロジェクト | プロジェクト終了時に即時失効 | KM-4, KM-7, ID-8 | 知見の蓄積不可・再利用困難 |

```yaml
decision:
  id: DC-5
  title: "メモリ保持・忘却（TTL・スコープ）"
  options:
    - id: session_only
      name: "セッションスコープのみ"
      patterns: [KM-4]
      pros: [漏洩リスク最小, 実装簡易]
      cons: [パーソナライズ不可, 毎回再説明]
      pick_when: ["一時的タスク", "高機密環境"]
    - id: rolling_ttl
      name: "ローリングTTL（90日）"
      patterns: [KM-4, ID-8]
      pros: [パーソナライズ, 業務効率向上]
      cons: [鮮度管理必要, ストレージコスト]
      pick_when: ["継続利用", "個人アシスタント"]
    - id: lifecycle_bound
      name: "ライフサイクル連動失効"
      patterns: [KM-4, KM-7, ID-8]
      pros: [退職・異動時の自動クリーンアップ]
      cons: [人事システム連携が前提]
      pick_when: ["プロジェクト単位", "人事イベント連動"]
  default_recommendation: "個人スコープは90日ローリングTTL、プロジェクトスコープはライフサイクル連動で設計"
```
