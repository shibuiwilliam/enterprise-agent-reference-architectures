---
title: "TO-9 コネクタ自前構築 vs 既存 iPaaS 再利用"
description: "既存統合資産の認可粒度が権限忠実要件を満たすか検証し、不足分のみMCP化する設計指針。"
status: done
---

# TO-9 コネクタ自前構築 vs 既存 iPaaS 再利用

## 概要

エージェントが外部システムやSaaSと連携する際、コネクタを自前で構築するか、Zapier・MuleSoft・Boomi等の既存iPaaS（Integration Platform as a Service）を再利用するかを選択する必要がある。原則は「既存資産があれば再利用、ただし認可粒度を必ず検証する」である。

## 比較

| 観点 | コネクタ自前構築 | 既存 iPaaS 再利用（[IN-4](../../patterns/in-integration/in4-existing-ipaas-reuse.md)） |
|---|---|---|
| 開発コスト | 高い | 低い（既存接続設定を活用） |
| 認可粒度の制御 | 任意に設計可能 | iPaaS の実装に依存 |
| 保守負担 | 自社持ち | iPaaSベンダー持ち（更新・障害対応） |
| エコシステム | ゼロから構築 | 既存フローを流用可能 |
| MCP対応 | [IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md) で標準化 | iPaaS側のMCP対応に依存 |

## 判断基準

**既存統合資産がある領域は再利用（[IN-4](../../patterns/in-integration/in4-existing-ipaas-reuse.md)）を優先する。** ただし再利用の前に以下の検証を行う。

再利用可否の判断軸：

- **認可粒度**：iPaaSの既存コネクタが、権限忠実（[ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md)）の要件を満たすか確認する。「管理者権限でSaaS全体にアクセスするサービスアカウントが埋め込まれている」コネクタは、ユーザー権限の縮退ができないため再利用不可と判断する。
- **監査証跡**：iPaaS経由の操作がエージェント側の監査ログと紐付けられるか確認する。操作者・操作内容・タイムスタンプが追跡できない場合は自前実装が必要になる場合がある。
- **User OBO対応**：[ID-2](../../patterns/id-identity/id2-identity-federation-obo.md) のToken Exchangeに対応しているかを確認する。対応していなければ再利用範囲を限定する。

新規・独自の統合ポイントは MCP化（[IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md)）を標準とする。MCPはツール定義を標準化し、将来的な差し替えや拡張を容易にする。

!!! warning "認可粒度の検証を省略してはならない"
    既存iPaaSのコネクタが「便利だから」という理由で無検証で採用されると、管理者権限のサービスアカウントを使う設計が温存され、権限漏洩の原因になる。再利用の前に必ず認可粒度の検証を実施する。

## ハイブリッド・段階的アプローチ

認可粒度が満たされる範囲では既存iPaaSを再利用し、満たされない箇所のみ自前実装またはMCP化する組み合わせが現実的である。

1. 既存iPaaSのコネクタ一覧を洗い出し、認可粒度・監査証跡の観点でスコアリングする。
2. 要件を満たすコネクタはそのまま再利用し、エージェントのツールとして登録する。
3. 要件を満たさないコネクタは、MCP Gateway（[IN-1](../../patterns/in-integration/in1-tool-mcp-gateway.md)）経由で権限制御を追加するか、自前実装に切り替える。
4. 新規統合ポイントはMCPを標準として設計し、iPaaSとの接続もMCP Adapter経由で統一する。

## 関連パターン

- [IN-1 Enterprise Tool / MCP Gateway](../../patterns/in-integration/in1-tool-mcp-gateway.md)
- [IN-4 Existing iPaaS Reuse](../../patterns/in-integration/in4-existing-ipaas-reuse.md)
- [ID-4 Permission Mirror / Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md)
