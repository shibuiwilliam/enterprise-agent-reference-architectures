---
title: "前提概念"
description: "本リファレンス全体で使用する重要な専門用語と前提知識の定義。"
status: done
---

# 前提概念

本リファレンスの意思決定ページ群で繰り返し登場する重要概念を定義しています。各用語は初出の意思決定ページでもインライン定義していますが、ここでは横断的な参照として集約しています。

## アイデンティティ・認可

| 用語 | 定義 |
|---|---|
| **OBO（On-Behalf-Of）** | OAuth 2.0 Token Exchange（RFC 8693）等を用いて、依頼者本人の権限に縮退したトークンで下流サービスを呼び出す委譲方式です。→ [ID-D2](../decisions/id-identity/id-d2-delegation-method.md) |
| **混乱代理（Confused Deputy）** | 権限のある主体が、権限のない主体の要求を自身の権限で実行してしまうセキュリティ上の問題です。エージェントがサービスアカウントの過剰権限でユーザーの代理操作を行う場合に発生します。→ [ID-D2](../decisions/id-identity/id-d2-delegation-method.md) |
| **Permission Mirror** | 各SaaSの権限（ACL/ロール/グループ）をエージェント基盤側に同期したキャッシュです。**権威ソースではなく近似**であり、SaaSネイティブ認可の補完として機能します。→ [ID-D3](../decisions/id-identity/id-d3-permission-reduction.md) |
| **PDP / PEP** | Policy Decision Point（ポリシー判断点）/ Policy Enforcement Point（ポリシー施行点）のことです。認可判断のロジック（PDP）と、その判断を実行時に適用するゲート（PEP）を分離する設計です。→ [ID-D5](../decisions/id-identity/id-d5-authorization-method.md) |
| **Zanzibar / ReBAC** | Google が開発した関係ベースアクセス制御（ReBAC）システムです。「ユーザーXはドキュメントYのビューワーである」のような関係タプルで権限を表現します。SpiceDB・OpenFGA 等のOSS実装があります。→ [ID-D3](../decisions/id-identity/id-d3-permission-reduction.md)、[ID-D5](../decisions/id-identity/id-d5-authorization-method.md) |
| **ABAC** | Attribute-Based Access Control の略です。主体・リソース・環境の属性（部門、役職、時刻、機密度等）に基づいてアクセスを制御するモデルです。→ [ID-D5](../decisions/id-identity/id-d5-authorization-method.md) |

## データ・知識

| 用語 | 定義 |
|---|---|
| **SoR（System of Record）** | 業務データの正（マスター）を保持するシステムです。Salesforce（CRM）・Workday（HCM）・ServiceNow（ITSM）等が該当します。エージェントの書き込み境界はSoRの整合性保護の観点で設計されます。→ [RT-D3](../decisions/rt-runtime/rt-d3-side-effect-safety.md) |
| **モザイク効果（Mosaic Effect）** | 単体では非機密のデータが複数組み合わさることで機密情報を推測可能になる現象です。例：部署構成＋役職＋評価期間から個人の人事評価を推測できてしまいます。→ [KM-D5](../decisions/km-knowledge/km-d5-confidentiality-strength.md) |
| **DLP（Data Loss Prevention）** | 機密データの外部漏洩を検知・防止する仕組みです。エージェントのコンテキストに含まれる機密情報のマスキング・除去に適用されます。→ [KM-D5](../decisions/km-knowledge/km-d5-confidentiality-strength.md) |
| **DPA（Data Processing Agreement）** | データ処理契約のことです。LLMベンダーに対して入力データの学習利用禁止・処理後の削除等を契約上義務付ける文書です。→ [KM-D5](../decisions/km-knowledge/km-d5-confidentiality-strength.md) |

## セキュリティ・計算

| 用語 | 定義 |
|---|---|
| **TEE（Trusted Execution Environment）** | ハードウェアレベルでメモリを暗号化・隔離し、ホストOS・管理者からもデータを読めないようにする実行環境です。Confidential VM、NVIDIA Confidential GPU 等が該当します。LLM推論にはGPU Confidential Computingが必要であり、現状は高コスト・限定的です。→ [KM-D5](../decisions/km-knowledge/km-d5-confidentiality-strength.md) |
| **OPA / Cedar** | Open Policy Agent（Rego言語）とAWS Cedar（Permit/Forbidルール）のことです。ポリシーをコードとして記述・テスト・バージョン管理する基盤です。→ [ID-D5](../decisions/id-identity/id-d5-authorization-method.md) |

## 実行・オーケストレーション

| 用語 | 定義 |
|---|---|
| **Saga** | 分散トランザクションを一連のローカルトランザクション＋補償操作に分解するパターンです。複数SaaSにまたがる操作の部分失敗時にロールバックを保証します。→ [RT-D4](../decisions/rt-runtime/rt-d4-long-running-reliability.md) |
| **RACI** | Responsible（実行責任者）・Accountable（説明責任者）・Consulted（相談先）・Informed（報告先）の4役割でタスク責任分担を定義するマトリクスです。→ [RT-D1](../decisions/rt-runtime/rt-d1-single-vs-multi-agent.md) |
| **MCP（Model Context Protocol）** | LLMとツール/データソースの接続を標準化するプロトコルです。エージェントが外部システムを呼び出す際の共通インターフェースとして機能します。→ [IN-D1](../decisions/in-integration/in-d1-tool-gateway.md) |
| **GraphRAG** | ナレッジグラフとベクトル検索を組み合わせたRAG手法です。エンティティ間の関係性クエリに強みがあります。→ [KM-D2](../decisions/km-knowledge/km-d2-knowledge-normalization.md) |
