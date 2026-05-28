---
title: "TO-1 OBO委譲 vs サービスアカウント"
description: "権限忠実性・監査帰責・実装コストの三軸でUser OBO、Service Account、Agent Identity、Hybridの使い分けを決める判断基準。"
status: done
---

# TO-1 OBO委譲 vs サービスアカウント

## 概要

エージェントが Salesforce のレコードを読むとき、「田中さん本人として読む」のか「システム管理者アカウントで読む」のかで、見えるデータも監査ログの意味もまったく変わります。User OBO（本人の権限で委譲）、サービスアカウント（共有技術アカウント）、Agent Identity（エージェント固有の ID）、そしてこれらを組み合わせた Hybrid の4方式があります。どれを選ぶかは「誰の権限で動かし、誰に帰責するか」という一点で決まります。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-1
decision_rules:
  - condition: "purpose == 'personal_assistance' AND saas_supports_token_exchange == true"
    recommendation: obo
    reason: "本人権限の忠実な伝播が重要。SaaS側の監査ログで帰責可能（RFC 8693 Token Exchange）"
  - condition: "purpose == 'department_service' AND multiple_approvers == true"
    recommendation: agent_identity
    reason: "複数名が関与する業務でも、エージェントIDに部門スコープを付与して権限を制御する"
  - condition: "purpose == 'company_batch'"
    recommendation: service_account
    reason: "全社バッチ・定常処理は Service Account を使うが、操作スコープと監査証跡を別途強化する"
  - condition: "operation_risk == 'high' AND irreversibility == 'irreversible'"
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

業務種別ごとに推奨パターンが異なります。

- **個人業務支援**：User OBOを選びます。担当者本人の権限でSaaSを操作し、権限の忠実な伝播と明確な帰責を保証します
- **部門代表業務**：Agent Identity＋部門ポリシーを選びます。複数名が関与する業務でも、エージェントIDに部門スコープを付与して権限を制御できます
- **全社バッチ・定常処理**：Service Account＋厳格な監査＋高リスクデータ分類を組み合わせます。Service Accountは権限が広がりやすいため、操作スコープと監査証跡を別途強化します
- **高リスク操作**：User OBO＋人間承認チェーン（[RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)）を組み合わせます。不可逆な操作や高額トランザクションは、委譲者本人の確認を経てから実行します

実務的に最も堅牢なアーキテクチャは「**実行主体は Agent、権限上限は User**」の Hybrid です。エージェントが作業を代行しつつ、User が持つ権限の上限を超えられない制約を実行基盤で保証します。

## ハイブリッド・段階的アプローチ

まず Service Account で動く既存ツールをそのまま活用し、高リスク操作に限って User OBO を導入するという移行経路が現実的です。Hybrid は実装が複雑になるため、次の順序で段階的に整備します。

1. 既存 Service Account に SPIFFE/SVID などの Workload Identity（[ID-3](../../patterns/id-identity/id3-workload-agent-identity.md)）を付与し、監査帰責を明確化します。
2. 高リスク操作のみ Token Exchange（RFC 8693）経由の User OBO に切り替えます。
3. 全操作を User OBO に対応させ、Service Account を廃止する方向で進めます。

Service Account の一本化は「万能サービスアカウント1個で全 SaaS を叩く」アンチパターンに直結します。運用が定着した段階で、スコープ分割か廃止に向けて必ず動いてください。

## 関連パターン

- [ID-2 Identity Federation & On-Behalf-Of](../../patterns/id-identity/id2-identity-federation-obo.md)
- [ID-3 Workload / Agent Identity](../../patterns/id-identity/id3-workload-agent-identity.md)
- [ID-4 Permission Mirror / Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md)
- [RT-4 Human Approval Chain](../../patterns/rt-runtime/rt4-human-approval-chain.md)

## 候補と推奨

| 状況／前提 | 推奨オプション | 必要パターン | 緩和トレードオフ |
|---|---|---|---|
| 個人業務の代理操作（読み書き） | OBO（A） | ID-2, ID-4, OB-2 | 実装複雑度↑ |
| 全社バッチ処理／単純集計 | サービスアカウント（B） | ID-3, ID-7, GV-9 | 過剰権限リスク↑ |
| 部門代表のシステム業務 | ハイブリッド（C） | ID-2, ID-3, RT-4 | 設計工数↑ |

```yaml
decision:
  id: TO-1
  title: "OBO委譲 vs サービスアカウント"
  options:
    - id: A
      name: "User-OBO"
      patterns: [ID-2, ID-4, OB-2]
      pros: [権限忠実, 本人帰責, 監査追跡可能]
      cons: [実装複雑, レガシー非対応]
      pick_when: ["複数SaaSの本人代理操作", "監査要件強"]
    - id: B
      name: "Service Account"
      patterns: [ID-3, ID-7, GV-9]
      pros: [実装容易, バッチ処理向き]
      cons: [過剰権限, 帰責曖昧]
      pick_when: ["バッチ処理", "公開情報のみ"]
    - id: C
      name: "Hybrid"
      patterns: [ID-2, ID-3, RT-4]
      pros: [現実的, 帰責明確]
      cons: [設計工数増]
      pick_when: ["部門代表業務", "段階導入"]
  default_recommendation: "C (Hybrid) for departmental Spokes; A for personal Copilots"
```
