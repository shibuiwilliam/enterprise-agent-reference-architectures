---
title: "部門別 適用例"
description: "Sales/HR/CS/Engineering/Executive の各部門エージェントに適用する重要パターンの束。"
status: done
---

# 部門別 適用例

各部門エージェントに適用する重要パターンの組み合わせを示す。部門ごとにリスク・データ・SaaS・承認構造が異なるため、適用するパターンの束も変わる。

## Sales Agent

**対象 SaaS**：Salesforce / Slack / Google Workspace / Sansan / Zoom

| パターン | 適用理由 |
|---|---|
| [ID-2 OBO](../patterns/id-identity/id2-identity-federation-obo.md) | 営業担当本人の権限で Salesforce にアクセス |
| [ID-4 Permission Mirror](../patterns/id-identity/id4-permission-mirror-least-of.md) | 担当外の顧客情報へのアクセス防止 |
| [IN-2 SaaS Adapter](../patterns/in-integration/in2-saas-connector-adapter.md) | Salesforce/Sansan の API 差を吸収 |
| [KM-5 Purpose-Bound Context](../patterns/km-knowledge/km5-purpose-bound-context.md) | 商談フォローアップに必要な文脈のみ |
| [RT-5 Command Envelope](../patterns/rt-runtime/rt5-command-envelope.md) | CRM 更新を構造化コマンドで実行 |
| [RT-4 Human Approval](../patterns/rt-runtime/rt4-human-approval-chain.md) | 見積・契約変更は上長承認 |

## HR Agent

**対象 SaaS**：Workday / Talentio / Google Workspace / Slack / 社内 HR システム

| パターン | 適用理由 |
|---|---|
| [KM-4 Scoped Memory](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) | 人事情報のスコープ分離（個人/部門/全社） |
| [KM-6 DLP & Redaction](../patterns/km-knowledge/km6-dlp-redaction-boundary.md) | 給与・評価情報のマスキング |
| [RT-4 Human Approval](../patterns/rt-runtime/rt4-human-approval-chain.md) | 人事異動・給与変更は二者承認 |
| [GV-4 Industry Policy Pack](../patterns/gv-governance/gv4-industry-policy-pack.md) | 労働法・個人情報保護法の準拠 |
| [RT-6 SoR Write Boundary](../patterns/rt-runtime/rt6-sor-write-boundary.md) | Workday への書き込みは正規手続き経由 |

## Customer Support Agent

**対象 SaaS**：Zendesk / Shopify / Salesforce / 製品 DB / 契約 DB

| パターン | 適用理由 |
|---|---|
| [ID-1 二面分離](../patterns/id-identity/id1-workforce-customer-split.md) | 顧客面と社内面の完全分離 |
| [RT-3 Risk-Tiered Autonomy](../patterns/rt-runtime/rt3-risk-tiered-autonomy.md) | 回答は自動、返金は承認付き |
| [KM-1 Access-Controlled RAG](../patterns/km-knowledge/km1-access-controlled-rag.md) | 製品 FAQ・ナレッジベースの権限付き検索 |
| [RT-7 Saga](../patterns/rt-runtime/rt7-enterprise-saga.md) | 返品・返金の複数システム更新 |
| [RT-9 Work Queue](../patterns/rt-runtime/rt9-work-queue-agent.md) | チケットキューの人間＋AI 協働 |

## Engineering Agent

**対象 SaaS**：GitHub / Jira / Linear / Slack / CI-CD / Cloud

| パターン | 適用理由 |
|---|---|
| [IN-1 Tool/MCP Gateway](../patterns/in-integration/in1-tool-mcp-gateway.md) | 開発ツール接続の統制 |
| [ID-6 Zero-Trust + Sandbox](../patterns/id-identity/id6-zero-trust-pdp-pep.md) | コード実行のサンドボックス隔離 |
| [RT-8 Durable Workflow](../patterns/rt-runtime/rt8-durable-workflow.md) | CI/CD パイプラインとの統合 |
| [OB-1 Observability Lake](../patterns/ob-observability/ob1-observability-lake.md) | 開発エージェントの行動トレース |
| [GV-9 Incident Response](../patterns/gv-governance/gv9-incident-response-kill-switch.md) | 本番影響時の即時停止 |
| [ID-7 Policy-as-Code](../patterns/id-identity/id7-policy-as-code-guardrail.md) | 本番デプロイの自動認可チェック |

## Executive Agent

**対象 SaaS**：DWH / Finance / Sales / HR / Portfolio

| パターン | 適用理由 |
|---|---|
| [KM-3 Canonical Object & KG](../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) | 経営ダッシュボード用の横断データ統合 |
| [KM-2 Context Mesh](../patterns/km-knowledge/km2-context-mesh.md) | 各部門データの権限付きフェデレーション |
| [KM-6 DLP & Redaction](../patterns/km-knowledge/km6-dlp-redaction-boundary.md) | 機密経営情報のマスキング |
| [GV-8 Cost Quota](../patterns/gv-governance/gv8-cost-quota-chargeback.md) | AI コストの全社可視化 |
| [GV-7 Evaluation Pipeline](../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) | 品質・業務適合性の継続計測 |
| [OB-2 Unified Audit](../patterns/ob-observability/ob2-unified-audit-lineage.md) | 厳格な監査（経営層は高リスク分類） |
