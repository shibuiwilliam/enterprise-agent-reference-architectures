---
title: "TO-4 Read-only vs Write-capable（段階的拡張）"
description: "参照系と更新系を明確に分離し、Read-onlyからHigh-risk Controlled Writeへ段階的に権限を拡張する設計指針。"
status: done
---

# TO-4 Read-only vs Write-capable（段階的拡張）

## 概要

「レコードを検索する」のと「レコードを更新する」のでは、失敗したときの被害がまるで違う。検索ミスはやり直せるが、間違った金額で請求書を発行すれば取り消しが効かない場合もある。エージェントの書き込み権限は「Read-only → Draft-only → 承認付き Write → 自動 Write」と段階的に広げるのが鉄則だ。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-4
decision_rules:
  - condition: "operation_type == 'read' AND human_review_before_use == true"
    recommendation: read_only
    reason: "情報検索・レポート生成・分析は自律実行してよい。誤った結果を出しても人間が確認してから使用するため不可逆な被害が生じにくい"
  - condition: "operation_type == 'write' AND irreversible == false AND operation_frequency == 'high' AND eval_complete == true"
    recommendation: auto_write_low_risk
    reason: "低リスク・高頻度の繰り返し操作はevalとカナリアリリースで安全性を確認後に自動Writeへ昇格する"
  - condition: "operation_type == 'write' AND irreversible == true AND approval_workflow_available == true"
    recommendation: approved_write
    reason: "不可逆な書き込みはSystem of Record経由で変更ログを残し、かつ人間の確認を挟む構造にする"
  - condition: "system_of_record == 'erp_crm_hr' OR financial_impact == true"
    recommendation: high_risk_controlled_write
    reason: "基幹業務システムや金融操作はSoR＋HitLの組み合わせを維持し、高リスク操作は自動化の対象から除外するか最終段階に留める"
  - condition: "deployment_phase == 'initial'"
    recommendation: read_only
    reason: "まず全操作をRead-onlyで開始し、エージェントの動作を本番トレースで観測してから段階的に権限を拡大する"
```

## 比較

| 段階 | 説明 | 適用条件 |
|---|---|---|
| Read-only | 参照・閲覧のみ。書き込み不可 | 初期導入・リスク評価前 |
| Draft-only | 下書き生成のみ。人間が最終保存する | 文書作成支援・メール草稿 |
| 承認付き Write | 書き込みは人間承認後に実行 | 中リスク操作・承認フロー整備済み |
| 低リスク自動 Write | 定義済み低リスク操作のみ自動実行 | eval・カナリア・監査が整備済み |
| 高リスク統制 Write | SoR経由・HitL付きで高リスク操作を実行 | 全監査基盤・インシデント対応体制が整備済み |

## 判断基準

参照系と更新系を明確に分離することが原則だ。

- **参照系（Read-only）＝Autopilot**：情報検索・レポート生成・分析は自律実行してよい。誤った結果を出しても人間が確認してから使用するため、不可逆な被害が生じにくい
- **更新系（Write-capable）＝SoR経由（[RT-6](../../patterns/rt-runtime/rt6-sor-write-boundary.md)）＋HitL（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）のCopilot**：データ変更・外部システムへの書き込みは、System of Record経由で変更ログを残し、かつ人間の確認を挟む構造にする

段階的拡張の判断軸：

- 当該操作は不可逆か（不可逆＝より慎重な段階を維持する）
- 操作対象の影響範囲はどこまでか（広いほど上位の段階が必要）
- eval・カナリアによる動作検証が完了しているか
- 監査証跡が十分に整備されているか

## ハイブリッド・段階的アプローチ

全業務を同一段階で扱わず、操作種別ごとに段階を割り当てる。

1. まず全操作をRead-onlyで開始し、エージェントの動作を本番トレースで観測する。
2. 低リスク・高頻度の繰り返し操作（定型フォーム入力等）からDraft-only→承認付きWriteへ昇格する。
3. eval（[GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）とカナリアリリースで安全性を確認した操作のみ自動Writeに昇格する。
4. 高リスク操作はSoR＋HitLの組み合わせを維持し、自動化の対象から除外するか最終段階に留める。

## 関連パターン

- [RT-6 SoR Write Boundary](../../patterns/rt-runtime/rt6-sor-write-boundary.md)
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md)
- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)
