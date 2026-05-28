---
title: "TO-5 Copilot vs Autopilot"
description: "参照系APIはAutopilot、更新系APIはHitLのCopilotに明確に分離し、Autopilot化はeval・カナリア・監査が揃った領域から段階的に進める指針。"
status: done
---

# TO-5 Copilot vs Autopilot

## 概要

経営層は「エージェントに業務を任せきりにして人件費を削減したい」と考えがちです。しかし確率的に動作する LLM が Workday の給与データや SAP の発注を自律的に書き換え始めたら、たった1回の誤動作で取り返しがつかなくなります。「情報を探して提案する」（Copilot）と「判断して実行まで完了する」（Autopilot）は明確に分けるべきです。その分離線は「参照系か更新系か」という一点で引きます。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-5
decision_rules:
  - condition: "operation_type == 'read' AND eval_complete == true AND canary_passed == true"
    recommendation: autopilot
    reason: "操作が読み取り専用で誤動作しても不可逆な被害が生じず、eval・カナリア・監査証跡が整備されていればAutopilot適切"
  - condition: "operation_type IN ['write', 'delete', 'approve'] OR system_of_record == 'erp_crm_hr'"
    recommendation: copilot
    reason: "更新・削除・承認といった不可逆な操作や基幹業務システムへの書き込みはHitLのCopilotを維持する"
  - condition: "operation_risk == 'low' AND canary_passed == true AND kill_switch_available == true"
    recommendation: autopilot
    reason: "承認率が高く低リスクな操作にevalとカナリアを適用し、kill switchと監査証跡が整備された状態でAutopilot化する"
  - condition: "infrastructure_readiness == 'incomplete'"
    recommendation: copilot
    reason: "「整備が追いつく前にAutopilotにする」という判断が最大のリスク。全操作をCopilotで開始し段階的に拡張する"
  - condition: "operation_has_side_effects == true AND irreversibility == 'reversible'"
    recommendation: hybrid_per_operation
    reason: "同一エージェントでも操作種別ごとにCopilot/Autopilotを使い分けるハイブリッドが現実的"
```

## 比較

| 観点 | Copilot（業務支援） | Autopilot（業務代行） |
|---|---|---|
| 人間の関与 | 提案・確認・最終承認が必要 | 自律実行。人間の関与は例外時のみ |
| 向き | 更新系API・高リスク操作・不可逆操作 | 参照系API・低リスク操作・可逆操作 |
| 障害時の影響 | 人間がブロックするため最小化できる | 自動実行された誤操作がそのまま被害になる |
| 必要な整備 | 承認フロー（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)） | eval・カナリア・監査証跡・kill switch |
| ROI実現速度 | 遅い（人間のボトルネック） | 速い（ただし整備不足時は事故リスク） |

## 判断基準

**参照系API＝Autopilot、更新系API＝HitL（Human-in-the-Loop）のCopilot** が基本原則です。

Autopilotが適切な条件：

- 操作が読み取り専用であり、誤動作しても不可逆な被害が生じません。
- eval・カナリアリリース・監査証跡が整備されており、異常を即検知できます。
- 同等の操作を人間が繰り返し行っており、エージェントの動作を十分に検証済みです。

Copilot（HitL）を維持すべき条件：

- 更新・削除・承認といった不可逆な操作を含みます。
- 基幹業務システム（ERP・CRM・HRシステム等）への書き込みを行います。
- 操作ミスの影響が広範囲に及び、ロールバックが困難または不可能です。

Autopilot 化は焦らず段階的に進めます。「整備が追いつく前に Autopilot にする」という判断がもっとも大きなリスクです。

## ハイブリッド・段階的アプローチ

同一エージェントでも操作種別ごとに Copilot/Autopilot を使い分けるハイブリッドが現実的です。

1. まず全操作を Copilot モードで開始し、人間の承認パターンを観測します。
2. 承認率が高く（ほぼ必ず承認される）、かつ低リスクな操作を特定します。
3. 特定した操作に eval とカナリアを適用し、Autopilot 化の候補を絞り込みます。
4. kill switch（[GV-9](../../patterns/gv-governance/gv9-incident-response-kill-switch.md)）と監査証跡（[GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）が整備された状態で Autopilot 化します。
5. 定期的に eval を再実行し、動作に劣化があれば Copilot に戻します。

## 関連パターン

- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)
- [RT-6 SoR Write Boundary](../../patterns/rt-runtime/rt6-sor-write-boundary.md)
- [GV-7 Evaluation Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 更新系API・高リスク・不可逆操作 | Copilot（A） | RT-3, RT-4, DC-1 | ROI実現速度が遅い |
| 参照系API・eval済み・kill switch整備 | Autopilot（B） | RT-3, GV-7, GV-9 | 誤動作が直接被害に |
| 同一エージェントで操作種別ごとに分離 | ハイブリッド（C） | RT-3, RT-4, DC-1, GV-7 | 設計・運用の複雑度↑ |

```yaml
decision:
  id: TO-5
  title: "Copilot vs Autopilot"
  options:
    - id: A
      name: "Copilot (HitL)"
      patterns: [RT-3, RT-4, DC-1]
      pros: [安全, 人間が最終判断, 高リスク操作に適合]
      cons: [ROI実現が遅い, 人間がボトルネック]
      pick_when: ["更新系API", "基幹業務システム", "不可逆操作"]
    - id: B
      name: "Autopilot"
      patterns: [RT-3, GV-7, GV-9]
      pros: [高ROI, 人間の介在不要, スケーラブル]
      cons: [誤動作が直接被害, 整備不足時に事故リスク大]
      pick_when: ["参照系API", "eval・カナリア通過済み", "kill switch整備済み"]
    - id: C
      name: "Hybrid per Operation"
      patterns: [RT-3, RT-4, DC-1, GV-7]
      pros: [現実的, 操作種別ごとに最適化]
      cons: [設計・運用の複雑度増]
      pick_when: ["参照系と更新系が混在", "段階的Autopilot化"]
  default_recommendation: "全操作をCopilot(A)で開始し、承認率・リスクを観測してC経由でBへ段階的に移行"
```
