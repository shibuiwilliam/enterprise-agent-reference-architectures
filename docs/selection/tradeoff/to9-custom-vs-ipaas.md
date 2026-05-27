---
title: "TO-9 コネクタ自前構築 vs 既存 iPaaS 再利用"
description: "既存統合資産の認可粒度が権限忠実要件を満たすか検証し、不足分のみMCP化する設計指針。"
status: done
---

# TO-9 コネクタ自前構築 vs 既存 iPaaS 再利用

## 概要

MuleSoft や Workato で既に Salesforce 連携を構築済みなら、わざわざ一から書き直すのは無駄だ。ただし既存コネクタが「管理者権限のサービスアカウント1個で全 API を叩く」設計になっていないか要注意である。ユーザー単位の権限分離ができなければ、エージェント経由で権限を超えたデータにアクセスできてしまう。「既存資産を再利用できるか」の判断は、認可粒度の検証を経て初めて下せる。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-9
decision_rules:
  - condition: "existing_ipaas_connector == true AND authorization_granularity_verified == true AND audit_trail_linkable == true"
    recommendation: ipaas_reuse
    reason: "既存統合資産がある領域は再利用を優先する。ただし認可粒度と監査証跡の要件を検証後に判断する"
  - condition: "existing_ipaas_connector == true AND uses_admin_service_account == true"
    recommendation: custom_build
    reason: "管理者権限のサービスアカウントが埋め込まれているコネクタはユーザー権限の縮退ができないため再利用不可と判断する"
  - condition: "new_integration_point == true"
    recommendation: mcp_gateway
    reason: "新規・独自の統合ポイントはMCP化（IN-1）を標準とする。ツール定義を標準化し将来的な差し替えや拡張を容易にする"
  - condition: "ipaas_obo_support == false AND obo_required == true"
    recommendation: hybrid_validated_ipaas
    reason: "ID-2のToken Exchangeに対応していなければ再利用範囲を限定し、MCP Gateway経由で権限制御を追加する"
  - condition: "authorization_granularity_not_verified == true"
    recommendation: hybrid_validated_ipaas
    reason: "認可粒度の検証を省略してはならない。無検証での採用は管理者権限SAを使う設計を温存し権限漏洩の原因になる"
```

## 比較

| 観点 | コネクタ自前構築 | 既存 iPaaS 再利用（[IN-4](../../patterns/in-integration/in4-existing-ipaas-reuse.md)） |
|---|---|---|
| 開発コスト | 高い | 低い（既存接続設定を活用） |
| 認可粒度の制御 | 任意に設計可能 | iPaaS の実装に依存 |
| 保守負担 | 自社持ち | iPaaSベンダー持ち（更新・障害対応） |
| エコシステム | ゼロから構築 | 既存フローを流用可能 |
| MCP対応 | [IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md) で標準化 | iPaaS側のMCP対応に依存 |

## 判断基準

**既存統合資産がある領域は再利用（[IN-4](../../patterns/in-integration/in4-existing-ipaas-reuse.md)）を優先する。** ただし再利用の前に以下を検証する。

再利用可否の判断軸：

- **認可粒度**：iPaaSの既存コネクタが権限忠実（[ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md)）の要件を満たすか確認する。「管理者権限でSaaS全体にアクセスするサービスアカウントが埋め込まれている」コネクタはユーザー権限の縮退ができないため、再利用不可と判断する
- **監査証跡**：iPaaS経由の操作がエージェント側の監査ログと紐付けられるか確認する。操作者・操作内容・タイムスタンプが追跡できない場合は自前実装が必要になる
- **User OBO対応**：[ID-2](../../patterns/id-identity/id2-identity-federation-obo.md) のToken Exchangeに対応しているかを確認する。対応していなければ再利用範囲を限定する

新規・独自の統合ポイントは MCP化（[IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md)）を標準とする。ツール定義を標準化し、将来的な差し替えや拡張を容易にする利点がある。

!!! warning "認可粒度の検証を省略してはならない"
    既存iPaaSのコネクタが「便利だから」という理由で無検証に採用されると、管理者権限のサービスアカウントを使う設計が温存され、権限漏洩の原因になる。再利用の前に必ず認可粒度の検証を実施する。

## ハイブリッド・段階的アプローチ

認可粒度が満たされる範囲では既存iPaaSを再利用し、満たされない箇所のみ自前実装またはMCP化する組み合わせが現実的だ。

1. 既存iPaaSのコネクタ一覧を洗い出し、認可粒度・監査証跡の観点でスコアリングする。
2. 要件を満たすコネクタはそのまま再利用し、エージェントのツールとして登録する。
3. 要件を満たさないコネクタは、MCP Gateway（[IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md)）経由で権限制御を追加するか、自前実装に切り替える。
4. 新規統合ポイントはMCPを標準として設計し、iPaaSとの接続もMCP Adapter経由で統一する。

## 関連パターン

- [IN-1 Enterprise Tool / MCP Gateway](../../patterns/in-integration/in1-tool-mcp-gateway.md)
- [IN-4 Existing iPaaS Reuse](../../patterns/in-integration/in4-existing-ipaas-reuse.md)
- [ID-4 Permission Mirror / Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md)
