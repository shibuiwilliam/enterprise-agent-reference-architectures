---
title: "TO-5 Copilot vs Autopilot"
description: "参照系APIはAutopilot、更新系APIはHitLのCopilotに明確に分離し、Autopilot化はeval・カナリア・監査が揃った領域から段階的に進める指針。"
status: done
---

# TO-5 Copilot vs Autopilot

## 概要

経営層は「エージェントに業務を任せきりにして人件費を削減したい」と考えがちだ。しかし確率的に動作する LLM が Workday の給与データや SAP の発注を自律的に書き換え始めたら、たった1回の誤動作で取り返しがつかない。「情報を探して提案する」（Copilot）と「判断して実行まで完了する」（Autopilot）は明確に分けるべきであり、その分離線は「参照系か更新系か」で引く。

## 比較

| 観点 | Copilot（業務支援） | Autopilot（業務代行） |
|---|---|---|
| 人間の関与 | 提案・確認・最終承認が必要 | 自律実行。人間の関与は例外時のみ |
| 向き | 更新系API・高リスク操作・不可逆操作 | 参照系API・低リスク操作・可逆操作 |
| 障害時の影響 | 人間がブロックするため最小化できる | 自動実行された誤操作がそのまま被害になる |
| 必要な整備 | 承認フロー（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)） | eval・カナリア・監査証跡・kill switch |
| ROI実現速度 | 遅い（人間のボトルネック） | 速い（ただし整備不足時は事故リスク） |

## 判断基準

**参照系API＝Autopilot、更新系API＝HitL（Human-in-the-Loop）のCopilot** という分離を基本原則とする。

Autopilotが適切な条件：

- 操作が読み取り専用であり、誤動作しても不可逆な被害が生じない
- eval・カナリアリリース・監査証跡が整備されており、異常を即検知できる
- 同等の操作を人間が繰り返し行っており、エージェントの動作を十分に検証済みである

Copilot（HitL）を維持すべき条件：

- 更新・削除・承認といった不可逆な操作を含む
- 基幹業務システム（ERP・CRM・HRシステム等）への書き込みを行う
- 操作ミスの影響が広範囲に及び、ロールバックが困難または不可能

Autopilot化の拡張は焦らず段階的に進める。「整備が追いつく前にAutopilotにする」という判断が最大のリスクである。

## ハイブリッド・段階的アプローチ

同一エージェントでも操作種別ごとにCopilot/Autopilotを使い分けるハイブリッドが現実的である。

1. 全操作をCopilotモードで開始し、人間の承認パターンを観測する。
2. 承認率が高く（ほぼ必ず承認される）、かつ低リスクな操作を特定する。
3. 特定した操作にevalとカナリアを適用し、Autopilot化の候補を絞り込む。
4. kill switch（[GV-9](../../patterns/gv-governance/gv9-incident-response-kill-switch.md)）と監査証跡（[GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）が整備された状態でAutopilot化する。
5. 定期的にevalを再実行し、動作の劣化があればCopilotに戻す。

## 関連パターン

- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)
- [RT-6 SoR Write Boundary](../../patterns/rt-runtime/rt6-sor-write-boundary.md)
- [GV-7 Evaluation Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)
