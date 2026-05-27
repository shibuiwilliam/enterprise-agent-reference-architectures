---
title: "TO-1 OBO委譲 vs サービスアカウント"
description: "権限忠実性・監査帰責・実装コストの三軸でUser OBO、Service Account、Agent Identity、Hybridの使い分けを決める判断基準。"
status: done
---

# TO-1 OBO委譲 vs サービスアカウント

## 概要

エージェントが Salesforce のレコードを読むとき、「田中さん本人として読む」のか「システム管理者アカウントで読む」のかで、見えるデータも監査ログの意味もまったく変わる。User OBO（本人の権限で委譲）、サービスアカウント（共有技術アカウント）、Agent Identity（エージェント固有の ID）、そしてこれらを組み合わせた Hybrid の4方式がある。どれを選ぶかは「誰の権限で動かし、誰に帰責するか」で決まる。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-1
decision_rules:
  - condition: "purpose == 'personal_assistance' AND saas_supports_token_exchange"
    recommendation: obo
    reason: "本人権限の忠実な伝播が重要。SaaS側の監査ログで帰責可能（RFC 8693 Token Exchange）"
  - condition: "purpose == 'department_representative' AND multiple_approvers == true"
    recommendation: agent_identity
    reason: "複数名が関与する業務でも、エージェントIDに部門スコープを付与して権限を制御する"
  - condition: "purpose == 'company_wide_batch' OR purpose == 'scheduled_job'"
    recommendation: service_account
    reason: "全社バッチ・定常処理は Service Account を使うが、操作スコープと監査証跡を別途強化する"
  - condition: "operation_risk == 'high' AND irreversible == true"
    recommendation: hybrid
    reason: "不可逆な高リスク操作は User OBO＋人間承認チェーンを組み合わせ、エージェントはUserの権限上限を超えない"
  - condition: "existing_service_account == true AND migration_phase == 'early'"
    recommendation: service_account
    reason: "移行初期は既存SAにWorkload Identity（SPIFFE/SVID）を付与し、高リスク操作のみUser OBOへ段階的に移行する"
```

## 比較

| 観点 | User OBO（[ID-2](../../patterns/id-identity/id2-identity-federation-obo.md)） | Service Account | Agent Identity（[ID-3](../../patterns/id-identity/id3-workload-agent-identity.md)） | Hybrid |
|---|---|---|---|---|
| 権限忠実性 | 高（委譲者の権限上限に縮退） | 低（判定バグ＝権限漏洩） | 中（エージェント固有ポリシーで制御） | 高（UserをceilingにAgentが実行） |
| 対応範囲 | 委譲対応SaaSのみ | どのAPIでも利用可 | 自律ジョブ・バッチ | 広い |
| 監査帰責 | 本人に明確 | 曖昧になりがち | エージェントIDに明確 | 明確（UserとAgentの両方を記録） |
| 実装 | 複雑（Token Exchange・RFC 8693が必要） | 容易 | 中程度 | 複雑 |

## 判断基準

業務種別ごとに推奨パターンが異なる。

- **個人業務支援**：User OBOを選ぶ。担当者本人の権限でSaaSを操作し、権限の忠実な伝播と明確な帰責を保証する
- **部門代表業務**：Agent Identity＋部門ポリシーを選ぶ。複数名が関与する業務でも、エージェントIDに部門スコープを付与して権限を制御できる
- **全社バッチ・定常処理**：Service Account＋厳格な監査＋高リスクデータ分類を組み合わせる。Service Accountは権限が広がりやすいため、操作スコープと監査証跡を別途強化する
- **高リスク操作**：User OBO＋人間承認チェーン（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）を組み合わせる。不可逆な操作や高額トランザクションは、委譲者本人の確認を経てから実行する

最も実務的なアーキテクチャは「**実行主体はAgent、権限上限はUser**」のHybridだ。エージェントが作業を代行しつつ、Userが持つ権限の上限を超えられない制約を実行基盤で保証する。

## ハイブリッド・段階的アプローチ

まずService Accountで動く既存ツールをそのまま活用し、高リスク操作に限ってUser OBOを導入するという移行経路が現実的だ。Hybridは実装が複雑になるため、以下の順序で段階的に整備する。

1. 既存Service AccountにSPIFFE/SVIDなどのWorkload Identity（[ID-3](../../patterns/id-identity/id3-workload-agent-identity.md)）を付与して監査帰責を明確化する。
2. 高リスク操作のみToken Exchange（RFC 8693）経由のUser OBOに切り替える。
3. 全操作をUser OBOに対応させ、Service Accountを廃止する方向で進める。

Service Account一本化は「万能サービスアカウント1個で全SaaSを叩く」アンチパターンに直結する。運用が定着した段階で必ずスコープ分割か廃止を図りたい。

## 関連パターン

- [ID-2 Identity Federation & On-Behalf-Of](../../patterns/id-identity/id2-identity-federation-obo.md)
- [ID-3 Workload / Agent Identity](../../patterns/id-identity/id3-workload-agent-identity.md)
- [ID-4 Permission Mirror / Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md)
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md)
