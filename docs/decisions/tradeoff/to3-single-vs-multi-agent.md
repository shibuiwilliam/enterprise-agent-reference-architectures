---
title: "TO-3 単一エージェント vs RACI マルチエージェント"
description: "「複雑だから」でなく「企業内の責任分担が複数に分かれるから」をマルチエージェント化の唯一の正当な基準とする選定指針。"
status: done
---

# TO-3 単一エージェント vs RACI マルチエージェント

## 概要

「処理が複雑だからマルチエージェントにしよう」は、エンタープライズでよくある過剰設計の入り口です。マルチにすればコストは N 倍になり、レイテンシは加算され、障害点も増えます。マルチ化が正当化されるのは「技術的に複雑だから」ではありません。「営業・法務・財務のように、企業内の責任分担が複数の部門に分かれるから」——これが唯一の正当な理由です。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-3
decision_rules:
  - condition: "responsibility_spans_multiple_departments == false AND latency_sensitive == true"
    recommendation: single_agent
    reason: "まず単一エージェントから始める。責任分担の主体が一つの部門・役割に収まるならマルチ化は過剰設計"
  - condition: "responsibility_spans_multiple_departments == true AND multiple_approvers == true"
    recommendation: multi_agent
    reason: "複数部門が関与し、それぞれの承認・責任が独立している業務はマルチエージェント化の唯一の正当な基準"
  - condition: "subtasks_require_different_toolsets == true"
    recommendation: multi_agent
    reason: "専門分野が異なるサブタスクにそれぞれ適したモデル・ツールセットが必要な場合はマルチ化が適切"
  - condition: "team_multi_agent_experience == 'low' OR latency_sensitive == true"
    recommendation: single_agent
    reason: "マルチエージェント運用経験が乏しく障害対応コストが見通せない場合、または可用性要件が厳しい場合は単一を維持する"
  - condition: "single_agent_bottleneck_identified == true AND responsibility_split_boundary_clear == true"
    recommendation: multi_agent
    reason: "単一エージェントで稼働しながら責任の境界が生じた箇所のみをサブエージェントとして段階的に分離する"
```

## 比較

| 観点 | 単一エージェント | RACI マルチエージェント（[RT-2](../../patterns/rt-runtime/rt2-raci-multi-agent.md)） |
|---|---|---|
| 実装コスト | 低 | 高（オーケストレーション・通信基盤が必要） |
| レイテンシ | 低 | 高（エージェント間の協調コストが加算） |
| 障害点 | 少ない | 多い（各エージェント・通信路が障害点） |
| 責任の明確化 | 一点に集中 | RACI で役割を分離できる |
| 向き | 単純Q&A・低遅延・低コスト | 複数部門関与・専門分化・高責任業務 |

## 判断基準

**まず単一エージェントから始めます。** マルチ化の判断基準は「処理が複雑だから」ではありません。唯一の正当な基準は「**企業内の責任分担が複数の部門・役割に分かれるから**」（[RT-2](../../patterns/rt-runtime/rt2-raci-multi-agent.md)）です。

マルチエージェントが適切な条件：

- 複数部門が関与し、それぞれの承認・責任が独立している業務。
- 専門分野が異なるサブタスクが存在し、それぞれに適したモデル・ツールセットが異なる場合。
- 最終承認責任者が明確に分かれており、単一エージェントでは帰責が曖昧になる業務。

単一エージェントを維持すべき条件：

- 処理が複雑でも、責任分担の主体が一つの部門・役割に収まる場合。
- レイテンシや可用性の要件が厳しく、分散処理のオーバーヘッドを許容できない場合。
- チームのマルチエージェント運用経験が乏しく、障害対応コストが見通せない段階。

## ハイブリッド・段階的アプローチ

単一エージェントで稼働させながらボトルネックや責任の分割点を観測し、必要な箇所だけを切り出す段階的拡張が現実的な進め方です。

1. まず単一エージェントでプロトタイプを構築し、責任の境界が生じる業務フローを特定します。
2. 責任分担が明確になった部分だけをサブエージェントとして分離します。
3. オーケストレーター（[RT-1](../../patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md)）とコスト・クォータ管理（[GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)）を整備してから、マルチ化を完成させます。

## 関連パターン

- [RT-2 RACI Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md)
- [RT-1 Org-Hierarchical Hub-and-Spoke](../../patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md)
- [GV-8 Cost / Quota / Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 責任主体が単一部門・低遅延要件 | 単一エージェント（A） | RT-1, GV-8 | 複雑業務への対応限界 |
| 複数部門の承認・責任が独立 | RACIマルチエージェント（B） | RT-2, RT-1, GV-8 | コスト・レイテンシ・障害点↑ |
| 段階的に責任分割点を特定 | 段階的分離（C） | RT-1, RT-2, GV-7 | 分離判断の工数 |

```yaml
decision:
  id: TO-3
  title: "単一エージェント vs RACI マルチエージェント"
  options:
    - id: A
      name: "Single Agent"
      patterns: [RT-1, GV-8]
      pros: [実装容易, 低レイテンシ, 障害点少]
      cons: [責任分担が曖昧になりやすい, 複雑業務に限界]
      pick_when: ["責任主体が単一部門", "低遅延要件", "運用経験が浅い"]
    - id: B
      name: "RACI Multi-Agent"
      patterns: [RT-2, RT-1, GV-8]
      pros: [責任明確, 専門分化, 帰責分離]
      cons: [コストN倍, レイテンシ加算, 障害点増]
      pick_when: ["複数部門が関与", "承認責任が独立", "専門ツールセットが異なる"]
    - id: C
      name: "Incremental Split"
      patterns: [RT-1, RT-2, GV-7]
      pros: [現実的, ボトルネック特定後に分離]
      cons: [分離判断に工数]
      pick_when: ["プロトタイプ段階", "責任境界が未確定"]
  default_recommendation: "まず単一(A)で開始し、責任分担の境界が明確になった箇所のみ段階的に分離(C→B)"
```
