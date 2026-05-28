---
title: "項目設計と面（カテゴリ）分類"
description: "各パターンの共通記述スキーマ（8項目）と7面の分類設計を定義する。"
status: done
---

# 項目設計と面（カテゴリ）分類

## 共通記述スキーマ

各パターンを以下の8項目で統一記述します。「価値仮説」は各パターンが企業価値のどこに効くかを明示するための項目であり、「落とし穴」は事故に直結しやすいため独立した明示項目として設けました。

| # | 項目 | 記述内容 |
|---|---|---|
| 1 | **概要** | 何であるかの一文要約 |
| 2 | **解決する企業課題** | どういう課題を解決するために、どのエンタープライズ固有の力（漏洩・サイロ・動的文脈・監査・コスト）に応えるか |
| 3 | **価値仮説** | このパターンがどの企業価値KPI（売上・利益／業務自動化／プロジェクト生産性／従業員効率／経営判断速度）に、どの経路で効くか。1〜3行で記載し、[GV-10](../decisions/gv-governance/gv-d7-value-measurement.md) の計測層と対応づける |
| 4 | **解決策と設計** | 課題の解決策と、それを実現する設計としての構造・データフロー・状態遷移・実装上の要点 |
| 5 | **向き／不向き** | 採用が効く条件と、害・過剰になる条件 |
| 6 | **要素技術・既存システム連携** | 代表技術・標準・対象SaaS |
| 7 | **落とし穴／選定の勘所** | 典型的な失敗と回避の指針 |
| 8 | **関連パターン** | 類似・補完・対比される他のパターンへのリンク |

!!! note "解決策と設計節の図"
    構造・データフロー・状態遷移・認可シーケンスは mermaid で記述します。特に [ID-2 OBO委譲](../decisions/id-identity/id-d2-delegation-method.md)、[ID-6 PDP/PEP](../decisions/id-identity/id-d5-authorization-method.md)、[RT-7 Saga](../decisions/rt-runtime/rt-d4-long-running-reliability.md)、[RT-10 イベント駆動](../decisions/rt-runtime/rt-d5-trigger-mechanism.md) はシーケンス/フロー図を推奨します。

## 面（カテゴリ）設計

パターンは「どの設計圧力に応えるか」で7面に分類しています。この分類は責務境界とも一致し、[リファレンスアーキテクチャ](../integration/architecture/index.md)の層構造にそのまま対応しています。

| 面 | テーマ | 主眼 | パターン数 |
|---|---|---|---|
| [面1 体験・ゲートウェイ (EX)](../decisions/ex-experience/ex-d1-front-door-channel.md) | 入口と提供面 | 仕事のある場所に届け、入口で統制する | 3 |
| [面2 制御・ガバナンス (GV)](../decisions/gv-governance/gv-d1-control-plane-scope.md) | 統治・統制 | 一元レジストリ・モデル統制・評価・コスト・事故対応 | 10 |
| [面3 アイデンティティ・信頼 (ID)](../decisions/id-identity/id-d1-workforce-customer-split.md) | 権限の忠実な伝播 | 誰の権限で動くかを保証する（全面の中で最も設計難度が高い） | 8 |
| [面4 実行・オーケストレーション (RT)](../decisions/rt-runtime/rt-d1-single-vs-multi-agent.md) | 分業・実行・自動化 | 責任分担・自律度・副作用・長尺・イベント | 11 |
| [面5 知識・メモリ・コンテキスト (KM)](../decisions/km-knowledge/km-d1-context-supply.md) | 漏らさず活かす | 権限を保ったまま横断文脈を供給 | 7 |
| [面6 統合・ツール (IN)](../decisions/in-integration/in-d1-tool-gateway.md) | 既存システム連携 | 作らず束ね、固有差を吸収 | 4 |
| [面7 観測・評価・監査 (OB)](../decisions/ob-observability/ob-d1-observability-scope.md) | 説明責任 | 三者帰責で全行為を再構成可能に | 2 |

### 面の読み方

面1〜2が「入口と統治」、面3が「権限の忠実な伝播（設計難度が高い）」、面4〜6が「実行と知識と連携」、面7が「説明責任」に当たります。積み上げる依存関係は[依存関係と依存チェーン](../integration/dependency-chain.md)で示します。

### エンタープライズ固有の設計圧力

設計圧力とは、一般的なソフトウェア設計ではあまり表面化しない、エンタープライズ固有の力のことです。

| 設計圧力 | 具体例 |
|---|---|
| **漏洩** | 顧客データの社外流出、部門間の不正アクセス、PII の外部LLM送信 |
| **サイロ** | SaaS間のデータ分断、部門間の語彙差、横断文脈の統合不能 |
| **動的文脈** | 人事異動・プロジェクト終了による権限変更、リアルタイムな組織構造の反映 |
| **監査** | 規制対応の証跡、インシデント原因究明、説明責任の確保 |
| **コスト** | LLMトークンの部門按分、マルチエージェントの推論爆発、SaaS APIレート消費 |

### 横断軸

7面に加えて、以下の2つが全面を貫く横断軸として機能します。

- **組織グラフ**：全面がスコープ・委譲・承認を組織構造から一貫して導く土台です。[ID-4](../decisions/id-identity/id-d3-permission-reduction.md)・[RT-1](../decisions/rt-runtime/rt-d1-single-vs-multi-agent.md)・[RT-4](../decisions/rt-runtime/rt-d2-autonomy-design.md)・[KM-4](../decisions/km-knowledge/km-d3-memory-scope.md) の根拠となります。
- **ゼロトラスト／監査**：全呼び出しを「人＋エージェント＋システム」の三者で認可・記録します。[ID-6](../decisions/id-identity/id-d5-authorization-method.md)・[OB-2](../decisions/ob-observability/ob-d2-audit-attribution.md) が中核を担います。

## フロントマター拡張（機械可読メタデータ）

本文の8項目スキーマに加え、各パターンページのフロントマター（YAML）に以下のフィールドを必須としています。コーディングエージェントはこのメタデータを `docs/_machine/patterns.json` から一括参照できます。

| フィールド | 型 | 説明 |
|---|---|---|
| `id` / `pattern_id` | string | パターンID（例：`ID-2`） |
| `applies_when` | list | 採用が有効な条件タグ |
| `not_applicable_when` | list | 採用が不適切な条件タグ |
| `decision_keys` | list | 参加する意思決定基準（DC/TO）のID |
| `value_drivers` | list | 効く企業価値ドライバ（下記語彙から選択） |
| `kpis` | list | GV-10 連携の代表指標 |
| `prerequisites` / `requires` | list | 依存する上流パターンのID |
| `related` / `required_by` | list | 双方向リンク対象のパターンID |
| `maturity_stage` | string | `foundation` / `execution` / `value_loop` のいずれか |
| `mvp` | string | 最小成立構成の一文説明 |
| `cost_orientation` | string | 相対コスト感 `S` / `M` / `L` |

### 価値ドライバ語彙（統一タグ）

全パターン・全部門事例の `value_drivers` フィールドで使用する語彙は、以下に統一しています。

| タグ | 意味 |
|---|---|
| `employee_efficiency` | 従業員の業務効率化 |
| `decision_quality` | 意思決定の質と速度向上 |
| `automation` | 業務プロセスの自動化 |
| `revenue_growth` | 売上・利益の成長 |
| `customer_value` | 顧客体験・満足度向上 |
| `audit_compliance` | 監査・コンプライアンスの確保 |
| `executive_decision` | 経営判断の加速 |
| `project_productivity` | プロジェクト生産性向上 |

### Decision Summary ブロック（末尾必須）

各パターンページの末尾に、以下の形式で機械可読かつ人間可読の Decision Summary YAML ブロックを配置します。

````markdown
## Decision Summary

```yaml
decision_summary:
  pattern: ID-2
  participates_in:
    - decision: TO-1
      role: option_a
  recommended_if:
    - "複数SaaSへ本人権限で書き込みが発生する"
  avoid_if:
    - "委譲を受理しないSaaS（ID-4で代替）"
  combines_with: [ID-4, KM-1, RT-5, OB-2]
  conflicts_with: []
  value_outcome:
    drivers: [audit_compliance, employee_efficiency]
    kpis: [監査追跡可能率, 誤アクセス事故件数]
  mvp: "主要2〜3 SaaSのみOBO化、残りはID-4で近似"
  cost: M
```
````

`scripts/build_machine_index.py` がこのブロックを抽出し、`docs/_machine/patterns.json` 等の機械可読 JSON を自動生成します。
