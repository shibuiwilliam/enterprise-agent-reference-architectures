---
title: "GV-1 Enterprise Agent Control Plane（レジストリ／ライフサイクル）"
description: "社内の全エージェントを登録・所有者明示・審査・版管理・廃止まで一元統制する制御プレーン。"
status: done
---

# GV-1 Enterprise Agent Control Plane（レジストリ／ライフサイクル）

## 概要

社内で稼働するすべてのエージェントを「誰が作り・何の目的で・どのデータに触れ・誰が責任を持つか」を明示して登録し、審査・版管理・廃止までのライフサイクルを一元管理する制御プレーンである。未登録のエージェント（シャドー AI）はモデルゲートウェイやエージェントゲートウェイで実行を遮断する。台帳ではなく「登録していなければ動かせない」実行許可のゲートとして機能する点が、単なるインベントリとの違いである。

## 解決する企業課題

エージェントが増殖すると「誰が作ったか分からない」「何を実行しているか把握できない」野良エージェント（シャドーAI）が組織に蔓延する。責任者が不明なエージェントはインシデント発生時に一次対応者を特定できず、事後調査が停止する。複数部門が同等機能を重複開発し、過剰権限を持つエージェントが承認なしに本番データを操作する。変更履歴が追跡できないため監査対応に多大な工数がかかる。エージェントが3個を超え複数チームが使い始めると、台帳なしでは統制不能になる——これが制御プレーンを持つ出発点である。

## 解決策と設計

各エージェントを一級オブジェクトとして定義し、登録から廃止までのライフサイクルを制御プレーンが一括管理する。登録＝実行許可のゲートとして機能させ、未登録エージェントは実行基盤・モデル Gateway（[GV-5](gv5-central-model-gateway.md)）で物理的に遮断する。

各エージェントに以下の属性を付与して管理する。

| 属性 | 説明 |
|---|---|
| owner / owner_department | 所有者・所有部門 |
| business_purpose | 業務目的 |
| allowed_users / allowed_projects | 利用許可ユーザー・プロジェクト |
| allowed_tools / data_domains | 利用許可ツール・データ領域 |
| risk_tier | リスク階層 |
| approval_policy | 承認ポリシー |
| audit_policy | 監査ポリシー |
| cost_budget | コスト予算 |

```mermaid
flowchart LR
    subgraph Lifecycle["エージェントライフサイクル"]
        REQ[登録申請] --> REV[審査<br/>セキュリティ/法務/データ保護]
        REV --> PUB[公開]
        PUB --> OP[運用<br/>監視/評価/版管理]
        OP --> DEP[廃止/アーカイブ]
    end

    subgraph Registry["Agent Registry"]
        DB[(エージェント台帳<br/>属性・版・状態)]
    end

    subgraph Enforcement["実行制御"]
        MGW[Model Gateway]
        GW[Agent Gateway]
        BLOCK[未登録は遮断]
    end

    REQ --> DB
    PUB --> DB
    DB --> MGW
    DB --> GW
    MGW --> BLOCK
    GW --> BLOCK
```

新規・変更は審査（セキュリティ・法務・データ保護）を経て公開する。未登録エージェントは実行基盤・モデル GW（[GV-5](gv5-central-model-gateway.md)）で遮断する。

## 向き／不向き

| 向き | 不向き |
|---|---|
| エージェントが3個を超え複数チームが利用 | 個人 PoC・実験段階 |
| 全社基盤として展開する場合 | 単一部門で1-2個のエージェントのみ |
| 監査・コンプライアンス要件がある場合 | 閉域の研究環境 |

## 要素技術・既存システム連携

- **レジストリ**：Agent Registry（カスタム or ServiceNow CMDB 拡張）
- **ポリシー管理**：Policy-as-Code（[ID-7](../id-identity/id7-policy-as-code-guardrail.md)）
- **既存 CMDB**：ServiceNow CMDB、サービスカタログとの統合
- **実行制御**：Model Gateway（[GV-5](gv5-central-model-gateway.md)）との連携で未登録遮断

## 落とし穴／選定の勘所

!!! warning "台帳止まりの罠"
    台帳を作っても実行制御と結びつけなければ形骸化する。登録＝実行許可のゲートにし、未登録は Model Gateway/Agent Gateway で物理的に遮断する。

- エージェントの「所有者」を明示し、インシデント時の一次対応者を常に特定できるようにする。
- 審査プロセスが重すぎると回避される。リスク階層に応じて審査の深さを変える（Tier 0-1 は軽量セルフサービス、Tier 3 以上は法務・セキュリティレビュー）。
- 廃止時はメモリ・権限・トークンの失効まで含めてライフサイクルを閉じる。

## 関連パターン

- [GV-2 Agent Catalog & Marketplace](gv2-agent-catalog-marketplace.md) — 補完：レジストリを土台にした社内カタログ。発見・申請の窓口として機能する
- [GV-5 Central Model Gateway](gv5-central-model-gateway.md) — 補完：未登録エージェントの遮断点として実行制御を担う
- [GV-8 Cost Quota & Chargeback](gv8-cost-quota-chargeback.md) — 補完：エージェント単位のコスト予算管理と連動する
- [OB-2 Unified Audit & Lineage](../ob-observability/ob2-unified-audit-lineage.md) — 補完：エージェント行為の監査証跡を提供する
- [ID-7 Policy-as-Code Guardrail](../id-identity/id7-policy-as-code-guardrail.md) — 補完：登録時のポリシー適用と実行時の強制を担う
