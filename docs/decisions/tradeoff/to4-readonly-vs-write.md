---
title: "TO-4 Read-only vs Write-capable（段階的拡張）"
description: "参照系と更新系を明確に分離し、Read-onlyからHigh-risk Controlled Writeへ段階的に権限を拡張する設計指針。"
status: done
---

# TO-4 Read-only vs Write-capable（段階的拡張）

## 概要

「レコードを検索する」のと「レコードを更新する」のでは、失敗したときの被害がまるで違います。検索ミスはやり直せます。しかし間違った金額で請求書を発行してしまえば、取り消しが効かない場合もあります。エージェントの書き込み権限は「Read-only → Draft-only → 承認付き Write → 自動 Write」と段階的に広げるのが鉄則です。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-4
decision_rules:
  - condition: "operation_type == 'read' AND audit_required == true"
    recommendation: read_only
    reason: "情報検索・レポート生成・分析は自律実行してよい。誤った結果を出しても人間が確認してから使用するため不可逆な被害が生じにくい"
  - condition: "operation_type == 'write' AND irreversibility == 'reversible' AND operation_frequency == 'high' AND eval_complete == true"
    recommendation: auto_write_low_risk
    reason: "低リスク・高頻度の繰り返し操作はevalとカナリアリリースで安全性を確認後に自動Writeへ昇格する"
  - condition: "operation_type == 'write' AND irreversibility == 'irreversible' AND approval_workflow_available == true"
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

参照系と更新系を明確に分離することが原則です。

- **参照系（Read-only）＝Autopilot**：情報検索・レポート生成・分析は自律実行してよいです。誤った結果を出しても人間が確認してから使用するため、不可逆な被害が生じにくいです。
- **更新系（Write-capable）＝SoR経由（[RT-6](../../patterns/rt-runtime/rt6-sor-write-boundary.md)）＋HitL（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）のCopilot**：データ変更・外部システムへの書き込みは System of Record 経由で変更ログを残し、かつ人間の確認を挟む構造にします。

段階的拡張の判断軸：

- その操作は不可逆か（不可逆なら、より慎重な段階を維持します）。
- 操作対象の影響範囲はどこまでか（広いほど上位の段階が必要です）。
- eval・カナリアによる動作検証が完了しているか。
- 監査証跡が十分に整備されているか。

## ハイブリッド・段階的アプローチ

全業務を同一段階で扱わず、操作種別ごとに段階を割り当てます。

1. まず全操作を Read-only で開始し、エージェントの動作を本番トレースで観測します。
2. 低リスク・高頻度の繰り返し操作（定型フォーム入力等）から Draft-only → 承認付き Write へ昇格します。
3. eval（[GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）とカナリアリリースで安全性を確認した操作のみ、自動 Write に昇格します。
4. 高リスク操作は SoR＋HitL の組み合わせを維持し、自動化の対象から除外するか最終段階に留めます。

## 関連パターン

- [RT-6 SoR Write Boundary](../../patterns/rt-runtime/rt6-sor-write-boundary.md)
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md)
- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 初期導入・リスク評価前 | Read-only（A） | RT-3, OB-1 | 業務自動化の範囲が限定的 |
| 低リスク定型操作・eval済み | 承認付きWrite（B） | RT-4, RT-6, GV-7 | 承認フローの運用負荷 |
| 全監査基盤整備済み・高頻度定型 | 自動Write（C） | RT-3, RT-6, GV-7, GV-9 | 誤操作時の影響範囲↑ |

```yaml
decision:
  id: TO-4
  title: "Read-only vs Write-capable（段階的拡張）"
  options:
    - id: A
      name: "Read-only"
      patterns: [RT-3, OB-1]
      pros: [安全, 即時導入可, 不可逆被害なし]
      cons: [業務自動化の範囲が限定的]
      pick_when: ["初期導入", "リスク評価未完了", "参照・分析業務"]
    - id: B
      name: "Approved Write"
      patterns: [RT-4, RT-6, GV-7]
      pros: [書き込み可能, 人間が最終確認]
      cons: [承認フローの運用負荷, レイテンシ]
      pick_when: ["中リスク操作", "承認フロー整備済み", "eval完了"]
    - id: C
      name: "Auto Write"
      patterns: [RT-3, RT-6, GV-7, GV-9]
      pros: [完全自動化, 高ROI]
      cons: [誤操作時の影響大, kill switch必須]
      pick_when: ["低リスク高頻度定型", "eval・カナリア通過済み", "監査基盤完備"]
  default_recommendation: "A (Read-only)で開始し、eval・カナリアを経てB→Cへ段階的に昇格"
```
