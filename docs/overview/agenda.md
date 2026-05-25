---
title: "はじめに：中心命題・分類学・組織グラフ・7面"
description: "エンタープライズAIエージェントの中心命題、エージェント分類学、組織グラフ、7面アーキテクチャ、標準整合を概観する。"
status: done
---

# はじめに：中心命題・分類学・組織グラフ・7面

## 中心命題

エンタープライズにAIエージェントを組み込む中心課題は「**AIを賢くすること**」ではなく、「**企業の既存のID・権限・責任・業務プロセス・監査・データ境界・組織構造の中に、新しい実行主体を安全に参加させ、売上・生産性・意思決定の向上という企業価値を引き出すこと**」である。安全に参加させることは前提条件であり、目的は企業価値の向上にある。

エンタープライズAIエージェントは単なるチャットUIではない。組織の権限構造を忠実に投影し、既存システムの真実（System of Record）を壊さずに束ね、すべての行為を企業横断で監査・統治できる形に閉じ込めた**管理可能・監査可能・権限制御された「デジタル業務主体」**である。そしてその安全な檻の中で解き放たれた知能が、受注率向上・業務自動化・意思決定加速・コスト最適化といった**企業価値を創出する実行主体**として機能する。

安全に動かすことは前提条件であり、目的は企業価値の向上にある。「誰の権限で・どのデータを・どう守って・誰の責任で」動かすかという統制設計（本書の7面・45パターン）と、「何の成果KPIを・どの経路で・いつまでに」動かすかという価値設計（[部門別適用例](../integration/departments/index.md)・[定着・アダプション](../integration/adoption.md)・[AI投資ポートフォリオ](../integration/portfolio.md)）は車の両輪である。

### 価値ループ：創出→計測→定着→再投資

統制設計（7面・45パターン）は安全な実行基盤を提供し、その上で価値が以下の4ステップを循環する。このループを回し続けることが企業価値向上の実体である。

```mermaid
flowchart LR
    subgraph ValueLoop["価値ループ"]
        CREATE["① 価値創出<br/>部門別ユースケース実行<br/>（Sales・CS・HR・Eng・Exec）"]
        MEASURE["② 計測<br/>GV-10 三層価値計測<br/>（定着→生産性→経営KPI）"]
        ADOPT["③ 定着<br/>チェンジマネジメント<br/>（採用→習慣化→拡大）"]
        REINVEST["④ 再投資<br/>AI投資ポートフォリオ<br/>（拡大・改善・撤退判断）"]
    end

    CREATE --> MEASURE
    MEASURE --> ADOPT
    ADOPT --> REINVEST
    REINVEST --> CREATE

    subgraph Foundation["統制基盤（7面・45パターン）"]
        CTRL["ID・権限・監査・ガバナンス"]
    end

    Foundation -.->|安全な実行基盤| ValueLoop
```

| ステップ | 担い手 | 主要ページ |
|---|---|---|
| ① 価値創出 | 部門別エージェントが成果KPIを動かす | [部門別適用例](../integration/departments/index.md)・[組み合わせレシピ](../integration/recipe.md) |
| ② 計測 | 定着率→生産性→経営KPIの3層で因果を追跡 | [GV-10 Three-Layer Value Measurement](../patterns/gv-governance/gv10-two-layer-value-measurement.md) |
| ③ 定着 | 利用率を引き上げ、ROIの分母を確保する | [定着・アダプション](../integration/adoption.md) |
| ④ 再投資 | 計測結果に基づき拡大・改善・撤退を判断 | [AI投資ポートフォリオ](../integration/portfolio.md)・[ユースケース選定ガイド](../integration/usecase-selection-guide.md) |

## AIエージェントは「企業内の実行主体」である

一般的なAIチャットは「回答主体」だが、エンタープライズエージェントは「業務実行主体」であり、企業システム上の**一級オブジェクト**として定義・管理する。

```text
EnterpriseAgent
- agent_id / owner_department / business_purpose
- allowed_users / allowed_projects / allowed_tools / allowed_data_domains
- risk_tier / approval_policy / memory_scope
- audit_policy / cost_budget / incident_owner
- model_version / prompt_version / policy_version
```

### エージェント分類学（役割の型）

| 分類 | 役割 | 例 |
|---|---|---|
| Employee Copilot | 従業員個人の業務支援 | メール下書き、資料作成、予定調整 |
| Department Agent | 部門業務の実行支援 | HR / Sales / Finance Agent |
| Project Agent | プロジェクト単位の作業支援 | PMO Agent、Issue Triage Agent |
| Process Agent | 業務プロセスの自動実行 | 稟議、請求、返金、オンボーディング |
| Customer-facing Agent | 顧客との対話・サポート | CS Agent、EC Agent |
| Governance Agent | 監査・リスク・品質管理 | Compliance / Security Review Agent |
| Platform Agent | 社内開発・運用支援 | SRE / Data / Dev Agent |

## 企業構造をアーキテクチャに反映する（組織グラフ）

企業はフラットなユーザー集合ではない。権限・メモリ・ログ・評価・コストは、組織の階層に紐づけて設計する。

```text
Company > Business Unit > Department > Section/Group > Team > Project > Subproject > Work Item
                                                                 └ Daily Operations
```

| スコープ | 対象 | 共有範囲 |
|---|---|---|
| User | 個人の嗜好・作業スタイル | 本人のみ |
| Team | チームルール・定例・タスク | チーム |
| Project | 決定事項・背景・成果物 | プロジェクト＋上位 |
| Department | 業務標準・KPI・手順・予算 | 部門 |
| Company | 全社規程・経営情報・全社ナレッジ | 全社 |
| Customer | 顧客別契約・問い合わせ・利用履歴 | 担当者・許可者 |

この構造を、Workday（組織・職位・レポートライン）、Okta/Entra ID（グループ）、Linear/Asana/Jira/Notion（プロジェクト）から名寄せした単一の**組織グラフ（Org Graph）**として管理し、すべての面がスコープ・委譲・共有・承認の根拠とする。

## 全体アーキテクチャ：7面と2つの横断軸

```mermaid
graph TB
    subgraph Users["ユーザー"]
        E[従業員 / 管理者 / 経営層]
        C[顧客 / パートナー]
    end

    subgraph F1["面1 体験・ゲートウェイ（EX）"]
        GW[Enterprise Agent Gateway<br/>認証/分類/リスク/レート/監査入口]
    end

    subgraph F3["面3 アイデンティティ・信頼（ID）"]
        IDP[IdP連携 / OBO・トークン交換 / ワークロードID]
        PDP[PDP/PEP / Permission Mirror / JIT資格情報]
    end

    subgraph F2["面2 制御・ガバナンス（GV）"]
        GOV[レジストリ / モデルGW / ポリシー / 評価 / コスト / 事故対応]
    end

    subgraph F4["面4 実行・オーケストレーション（RT）"]
        RT[Hub&Spoke / RACI / Risk-Tier / 承認 / Saga / 永続WF]
    end

    subgraph F5["面5 知識・メモリ（KM）"]
        KM[権限認識RAG / Context Mesh / 正規オブジェクト / スコープ記憶]
    end

    subgraph F6["面6 統合・ツール（IN）"]
        IN[Tool/MCP Gateway / SaaS Adapter / レート調停 / iPaaS]
    end

    subgraph SoR["System of Record"]
        S[Salesforce / ServiceNow / Workday / Slack / Box / Jira / Zendesk 等]
    end

    subgraph F7["面7 観測・評価・監査（OB）"]
        OB[Observability Lake / 統一監査・系譜（三者帰責）]
    end

    Users --> F1
    F1 --> F3
    F3 --> F2
    F2 --> F4
    F4 --> F5
    F5 --> F6
    F6 --> SoR
    SoR --> F7
```

各面の責務は以下のとおりである。

| 面 | テーマ | 主眼 | パターン数 |
|---|---|---|---|
| [面1 体験・ゲートウェイ (EX)](../patterns/ex-experience/index.md) | 入口と提供面 | 仕事のある場所に届け、入口で統制する | 3 |
| [面2 制御・ガバナンス (GV)](../patterns/gv-governance/index.md) | 統治・統制 | 一元レジストリ・モデル統制・評価・コスト・事故対応 | 10 |
| [面3 アイデンティティ・信頼 (ID)](../patterns/id-identity/index.md) | 権限の忠実な伝播 | 誰の権限で動くかを保証する（全面の中で最も設計難度が高い） | 8 |
| [面4 実行・オーケストレーション (RT)](../patterns/rt-runtime/index.md) | 分業・実行・自動化 | 責任分担・自律度・副作用・長尺・イベント | 11 |
| [面5 知識・メモリ・コンテキスト (KM)](../patterns/km-knowledge/index.md) | 漏らさず活かす | 権限を保ったまま横断文脈を供給 | 7 |
| [面6 統合・ツール (IN)](../patterns/in-integration/index.md) | 既存システム連携 | 作らず束ね、固有差を吸収 | 4 |
| [面7 観測・評価・監査 (OB)](../patterns/ob-observability/index.md) | 説明責任 | 三者帰責で全行為を再構成可能に | 2 |

!!! tip "読み方"
    面1〜2が「入口と統治」、面3が「権限の忠実な伝播（設計難度が高い）」、面4〜6が「実行と知識と連携」、面7が「説明責任」。これらを積み上げる依存関係は[依存関係と依存チェーン](../integration/dependency-chain.md)で示す。各パターンが**どの企業価値KPIに効くか**は各パターンの「価値仮説」節に記載し、部門ごとの具体的な成果KPIマッピングは[部門別適用例](../integration/departments/index.md)、導入の段階設計は[価値成熟度ロードマップ](../integration/value-maturity-roadmap.md)、初期ユースケースの選び方は[ユースケース選定ガイド](../integration/usecase-selection-guide.md)で扱う。

**横断軸**として以下の2つが全面を貫く。

- **組織グラフ**：全面がスコープ・委譲・承認を組織構造から一貫して導く土台。
- **ゼロトラスト／監査**：全呼び出しを「人＋エージェント＋システム」の三者で認可・記録する。

## 標準・フレームワークとの整合

エンタープライズでは、これらを「アプリ設計の指針」ではなく「**企業アーキテクチャ設計の制約**」として扱う。

| 標準・フレームワーク | 位置づけ |
|---|---|
| **NIST AI RMF（Generative AI Profile）** | 生成AI固有リスクの特定と管理アクション設計の枠組み |
| **OWASP Top 10 for LLM Applications** | Prompt Injection / Sensitive Information Disclosure / Excessive Agency / Unbounded Consumption 等を主要リスクとして整理 |
| **NIST SP 800-207 Zero Trust Architecture** | 境界でなく主体・資産・リソース中心の保護 |
| **OIDC / SCIM** | 既存ID標準（認証・プロビジョニング）の上に乗る。独自ID管理を乱立させない |
| **OAuth 2.0 Token Exchange（RFC 8693）** | 委譲・代理実行（OBO）の標準 |
| **OPA/Rego・Cedar** | Policy-as-Code による決定論的認可 |
| **MCP（Model Context Protocol）** | ツール接続の標準（企業ではGateway経由に統制） |
| **CloudEvents** | SaaS/社内イベントの共通記述 |
| **OpenTelemetry GenAI semantic conventions** | エージェント・モデル・ツール呼び出しの標準観測 |

### 標準・リスク項目 ⇔ パターン対応表

各標準やリスク項目が、本書のどのパターン・選定基準で対処されるかを以下に示す。

| 標準・リスク項目 | 対応パターン・選定基準 |
|---|---|
| **OWASP: Prompt Injection** | [ID-7 Policy-as-Code Guardrail](../patterns/id-identity/id7-policy-as-code-guardrail.md)、[TO-12 プロンプト vs 実行基盤](../selection/tradeoff/to12-prompt-vs-platform.md) |
| **OWASP: Sensitive Information Disclosure** | [KM-1 Access-Controlled RAG](../patterns/km-knowledge/km1-access-controlled-rag.md)、[KM-6 DLP & Redaction](../patterns/km-knowledge/km6-dlp-redaction-boundary.md)、[ID-1 二面分離](../patterns/id-identity/id1-workforce-customer-split.md) |
| **OWASP: Excessive Agency** | [RT-3 Risk-Tiered Autonomy](../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)、[RT-6 SoR Write Boundary](../patterns/rt-runtime/rt6-sor-write-boundary.md)、[ID-4 Permission Mirror](../patterns/id-identity/id4-permission-mirror-least-of.md) |
| **OWASP: Unbounded Consumption** | [DC-2 タイムアウト・リトライ・予算](../selection/degree/dc2-timeout-retry-budget.md)、[GV-8 Cost Quota & Chargeback](../patterns/gv-governance/gv8-cost-quota-chargeback.md) |
| **NIST AI RMF: 生成AIリスク管理** | [GV-7 Evaluation Pipeline](../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)、[GV-4 Industry Policy Pack](../patterns/gv-governance/gv4-industry-policy-pack.md)、[DC-1 自律度ティア](../selection/degree/dc1-risk-tier-boundary.md) |
| **NIST SP 800-207: Zero Trust** | [ID-6 Zero-Trust PDP/PEP](../patterns/id-identity/id6-zero-trust-pdp-pep.md)、[ID-2 OBO 委譲](../patterns/id-identity/id2-identity-federation-obo.md)、[ID-5 JIT Credentials](../patterns/id-identity/id5-jit-scoped-credentials.md) |
| **RFC 8693: Token Exchange** | [ID-2 OBO 委譲](../patterns/id-identity/id2-identity-federation-obo.md) |
| **OPA/Rego・Cedar** | [ID-7 Policy-as-Code Guardrail](../patterns/id-identity/id7-policy-as-code-guardrail.md) |
| **MCP** | [IN-1 Tool / MCP Gateway](../patterns/in-integration/in1-tool-mcp-gateway.md) |
| **CloudEvents** | [RT-10 Event-Driven Orchestrator](../patterns/rt-runtime/rt10-event-driven-orchestrator.md) |
| **OpenTelemetry** | [OB-1 Observability Lake](../patterns/ob-observability/ob1-observability-lake.md)、[OB-2 Unified Audit](../patterns/ob-observability/ob2-unified-audit-lineage.md) |

## 本書の歩き方

1. **本章**：命題・統合方針・基礎概念・7面アーキテクチャ・標準整合
2. **[項目設計と面分類](schema.md)**：各パターンの記述スキーマと面（カテゴリ）設計
3. **[パターンカタログ](../patterns/index.md)**：7面・計45パターンの本体（体験3＋ガバナンス10＋アイデンティティ8＋ランタイム11＋知識7＋統合4＋観測2）
4. **[「程度」の選定基準](../selection/degree/index.md)**：連続量パラメータの決め方（9項目）
5. **[「相反する仕組み」の選定基準](../selection/tradeoff/index.md)**：二者択一の判断軸（12項目）
6. **[統合と組み合わせ方](../integration/dependency-chain.md)**：依存関係・横断軸・組み合わせレシピ・部門別適用例・リファレンスアーキテクチャ
7. **[用語集](../glossary.md)**：専門用語の定義一覧
