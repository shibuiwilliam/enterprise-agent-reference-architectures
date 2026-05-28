---
title: "用語集（Glossary）"
description: "本サイトで使用する専門用語・略語の定義一覧。"
---

# 用語集（Glossary）

本サイトで使用する主要な専門用語を定義しています。各パターンページの初出箇所からリンクして参照できます。

| 用語 | 定義 |
|---|---|
| **OBO（On-Behalf-Of）** | OAuth 2.0 Token Exchange（RFC 8693）等を用いて、依頼者本人の権限に縮退したトークンで下流サービスを呼び出す委譲方式。→ [ID-2](patterns/id-identity/id2-identity-federation-obo.md) |
| **混乱代理（Confused Deputy）** | 権限のある主体が、権限のない主体の要求を自身の権限で実行してしまうセキュリティ上の問題。エージェントがサービスアカウントの過剰権限でユーザーの代理操作を行う場合に発生します。→ [ID-2](patterns/id-identity/id2-identity-federation-obo.md) |
| **モザイク効果（Mosaic Effect）** | 単体では非機密のデータが複数組み合わさることで機密情報を推測可能になる現象。例：座席表＋出張記録＋登記情報→未公開M&A接触先の推測。→ [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **Permission Mirror** | 各SaaSの権限（ACL/ロール/グループ）をエージェント基盤側に同期したキャッシュ。権威ソースではなく近似であり、SaaSネイティブ認可の補完として機能します。→ [ID-4](patterns/id-identity/id4-permission-mirror-least-of.md) |
| **Zanzibar** | Google が開発した関係ベースアクセス制御（ReBAC）システム。「ユーザーXはドキュメントYのビューワーである」のような関係タプルで権限を表現します。SpiceDB・OpenFGA 等のOSS実装があります。→ [ID-4](patterns/id-identity/id4-permission-mirror-least-of.md)、[ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md) |
| **ReBAC（Relationship-Based Access Control）** | リソース間の関係（所有者・メンバー・ビューワー等）に基づいてアクセスを制御するモデル。RBAC（ロールベース）やABAC（属性ベース）と組み合わせて使われます。→ [ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md) |
| **PDP / PEP** | Policy Decision Point（ポリシー判断点）/ Policy Enforcement Point（ポリシー施行点）。認可判断のロジック（PDP）と、その判断を実行時に適用するゲート（PEP）を分離する設計です。→ [ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md) |
| **DPA（Data Processing Agreement）** | データ処理契約。LLMベンダーに対して入力データの学習利用禁止・処理後の削除等を契約上義務付ける文書です。→ [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **TEE（Trusted Execution Environment）** | ハードウェアレベルでメモリを暗号化・隔離し、ホストOS・管理者からもデータを読めないようにする実行環境。Confidential VM、NVIDIA Confidential GPU 等が該当します。→ [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **Zeroization（ゼロ化）** | メモリ領域を暗号学的に安全な方法でクリアし、データの残留を防止する処理。揮発コンテキストのセッション終了時に適用されます。→ [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **SoR（System of Record）** | 業務データの正（マスター）を保持するシステム。Salesforce（CRM）・Workday（HCM）・ServiceNow（ITSM）等。エージェントの書き込み境界はSoRの整合性保護の観点で設計されます。→ [RT-6](patterns/rt-runtime/rt6-sor-write-boundary.md) |
| **Saga** | 分散トランザクションを一連のローカルトランザクション＋補償操作に分解するパターン。エージェントが複数SaaSにまたがる操作を行う際に、部分失敗時のロールバックを保証します。→ [RT-7](patterns/rt-runtime/rt7-enterprise-saga.md) |
| **RACI** | Responsible（実行責任者）・Accountable（説明責任者）・Consulted（相談先）・Informed（報告先）の4役割でタスクの責任分担を定義するマトリクスです。→ [RT-2](patterns/rt-runtime/rt2-raci-multi-agent.md) |
| **GraphRAG** | ナレッジグラフとベクトル検索を組み合わせたRAG手法。エンティティ間の関係性クエリ（「なぜその設計になったか」等）に強い特性があります。→ [KM-3](patterns/km-knowledge/km3-canonical-object-knowledge-graph.md)、[RT-11](patterns/rt-runtime/rt11-project-digital-twin.md) |
| **MCP（Model Context Protocol）** | LLMとツール/データソースの接続を標準化するプロトコル。エージェントが外部システムを呼び出す際の共通インターフェースとして機能します。→ [IN-1](patterns/in-integration/in1-tool-mcp-gateway.md) |
| **OPA（Open Policy Agent）** | 汎用ポリシーエンジン。Rego言語でポリシーを記述し、API・Kubernetes・データアクセス等の認可判断を統一的に行います。→ [ID-7](patterns/id-identity/id7-policy-as-code-guardrail.md) |
| **Cedar** | AWS が開発したポリシー言語・評価エンジン。Permit/Forbid ルールで細粒度の認可を記述します。Amazon Verified Permissions で利用されます。→ [ID-7](patterns/id-identity/id7-policy-as-code-guardrail.md) |
