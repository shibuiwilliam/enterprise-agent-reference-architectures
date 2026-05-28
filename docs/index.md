---
title: "ホーム"
description: "数万人規模の従業員・顧客と多様な既存SaaSを前提に、AIエージェントをエンタープライズへ安全に組み込むためのアーキテクチャパターン集。"
---

# エンタープライズAIエージェント・アーキテクチャ・リファレンス

エンタープライズにAIエージェントを組み込む中心課題は「**AIを賢くすること**」ではありません。「**価値を生むために動かし、壊さないために統べる**」——これが本質といえます。企業の既存のID・権限・責任・業務プロセス・監査・データ境界・組織構造の中に新しい実行主体を安全に参加させ、受注率向上・業務自動化・生産性改善・意思決定加速という**企業価値を引き出します**。安全はその土台であり、目的はあくまで企業価値の向上にあります。

本サイトは、数万人規模・多様な既存SaaS（Salesforce / ServiceNow / Workday / Okta / Slack / Box / Jira / Zendesk / Shopify / バクラク / Sansan ほか）・厳格な権限管理・階層的組織を前提とした実務リファレンスです。**45パターン（安全に動かす型）**と**価値運用ページ群（価値を出す型）**の二本立てで構成されます。

!!! note "本サイトの二重構造"
    **45パターン**（7面：体験3＋ガバナンス10＋アイデンティティ8＋ランタイム11＋知識7＋統合4＋観測2）がエージェントを**安全に動かす設計の型**を、**選定基準 21**（程度9＋トレードオフ12）が調整と判断軸を提供します。これに加え、**価値運用ページ群**（[価値成熟度ロードマップ](integration/value-maturity-roadmap.md)・[ユースケース選定ガイド](integration/usecase-selection-guide.md)・[GV-10 三層価値計測](patterns/gv-governance/gv10-two-layer-value-measurement.md)・[定着・アダプション](integration/adoption.md)・[AI投資ポートフォリオ](integration/portfolio.md)）が**価値を出す運用の型**を提供します。45パターンで安全を確保し、価値運用ページ群で成果を出す——この二重構造が本サイトの設計思想です。

## 本サイトの構成

<div class="grid cards" markdown>

- :material-flag-outline: **[はじめに](overview/agenda.md)**

    中心命題・エージェント分類学・組織グラフ・7面アーキテクチャ・標準整合。

- :material-shape-outline: **[パターンカタログ](patterns/index.md)**

    7面・45パターンを共通スキーマで記述。

- :material-tune-variant: **[「程度」の選定基準](decisions/degree/index.md)**

    自律度ティア・予算・ログ三層分離・ガードレール強度など連続量の決め方。

- :material-scale-balance: **[「相反する仕組み」の選定基準](decisions/tradeoff/index.md)**

    OBO/SA・中央レイク/Mesh・Copilot/Autopilot など二者択一の判断軸。

- :material-puzzle-outline: **[統合と組み合わせ方](integration/dependency-chain.md)**

    依存関係・横断軸・組み合わせレシピ・部門別適用例・リファレンスアーキテクチャ。

- :material-chart-line: **[価値運用ページ群（価値を出す型）](integration/value-maturity-roadmap.md)**

    [価値成熟度ロードマップ](integration/value-maturity-roadmap.md)（導入順序）・[ユースケース選定ガイド](integration/usecase-selection-guide.md)（初期ユースケースの選び方）・[GV-10 三層価値計測](patterns/gv-governance/gv10-two-layer-value-measurement.md)（ROI計測）・[定着・アダプション](integration/adoption.md)（チェンジマネジメント）・[AI投資ポートフォリオ](integration/portfolio.md)（再投資判断）・[価値実現のアンチパターン](integration/value-anti-patterns.md)（典型的な失敗と回避策）・[部門別適用例](integration/departments/index.md)（成果KPIマッピング）。

</div>

## 価値とROI（なぜAIエージェントを導入するのか）

エンタープライズAIエージェントが創出する企業価値は以下の5軸に集約されます。

| 価値軸 | 効果の例 | 関連ページ |
|---|---|---|
| **売上・利益改善** | 受注率向上・アップセル示唆・失注予兆検知 | [Sales Agent](integration/departments/sales.md)・[GV-10 価値計測（3層）](patterns/gv-governance/gv10-two-layer-value-measurement.md) |
| **業務自動化** | バックオフィスの端到端処理・定型業務のゼロタッチ化 | [組み合わせレシピ](integration/recipe.md)・[RT-10 イベント駆動](patterns/rt-runtime/rt10-event-driven-orchestrator.md) |
| **プロジェクト生産性** | リードタイム短縮・ボトルネック検知・情報共有の即時化 | [RT-11 デジタルツイン](patterns/rt-runtime/rt11-project-digital-twin.md)・[Engineering Agent](integration/departments/engineering.md) |
| **従業員効率** | 情報検索・ドラフト生成・トリアージの自動化 | [KM-1 権限認識RAG](patterns/km-knowledge/km1-access-controlled-rag.md)・[定着・アダプション](integration/adoption.md) |
| **経営判断の加速** | 全社KPI横断・シナリオ分析・リスク早期察知 | [Executive Agent](integration/departments/executive.md)・[AI投資ポートフォリオ](integration/portfolio.md) |

!!! tip "クイックウィン：90日で最初のROI"
    読み取り専用・低リスク・高頻度のユースケース（社内ナレッジ検索・議事録要約）から始め、最初の90日で経営に報告可能なROIを実証します。詳細は[組み合わせレシピの価値早期実現トラック](integration/recipe.md)を参照してください。

## 価値ループ：選定→クイックウィン→定着→計測→拡大→再投資

45パターンが安全な実行基盤を提供し、その上で価値が6ステップを循環します。このループを回し続けることで、企業価値の向上が実現します。

```mermaid
flowchart LR
    SELECT["① ユースケース選定<br/>高価値・低リスクの初手"]
    RECIPE["② 最小安全ベースライン<br/>＋クイックウィン"]
    ADOPT["③ 定着<br/>チェンジマネジメント"]
    MEASURE["④ GV-10 計測<br/>三層価値計測"]
    MATURE["⑤ 成熟度拡大<br/>段階的に自律度と範囲を拡張"]
    PORTFOLIO["⑥ ポートフォリオ<br/>再投資・改善・撤退"]

    SELECT --> RECIPE
    RECIPE --> ADOPT
    ADOPT --> MEASURE
    MEASURE --> MATURE
    MATURE --> PORTFOLIO
    PORTFOLIO --> SELECT
```

| ステップ | 担い手 | 主要ページ |
|---|---|---|
| ① ユースケース選定 | 高価値・低リスクの初手を選ぶ | [価値ユースケース選定ガイド](integration/usecase-selection-guide.md) |
| ② クイックウィン | MVP構成で30〜60日以内に初期価値を実証 | [組み合わせレシピ](integration/recipe.md) |
| ③ 定着 | 利用率を引き上げ、ROIの分母を確保する | [定着・アダプション](integration/adoption.md) |
| ④ 計測 | 定着率→生産性→経営KPIの3層で因果を追跡 | [GV-10 三層価値計測](patterns/gv-governance/gv10-two-layer-value-measurement.md) |
| ⑤ 成熟度拡大 | 段階的に適用範囲と自律度を拡大する | [価値成熟度ロードマップ](integration/value-maturity-roadmap.md) |
| ⑥ ポートフォリオ | 計測結果に基づき拡大・改善・撤退を判断 | [AI投資ポートフォリオ](integration/portfolio.md) |

## 本サイトの入口（人間向け／コーディングエージェント向け）

| 読者 | 入口 | 推奨ルート |
|---|---|---|
| **人間**（アーキテクト・推進責任者） | 本ページ → [意思決定の手引き](decisions/decision-guide.md) | シナリオから DC/TO を選び、推奨パターンを確認 |
| **コーディングエージェント** | リポジトリルートの `agents.md` → `docs/_machine/index.json` | 機械可読 JSON を参照し、出力テンプレートに従って提案を生成 |

## 価値ドライバ別逆引き索引

「何の価値に効くか」からパターンと部門事例を引きます。

| 価値ドライバ | 効くパターン | 部門事例 |
|---|---|---|
| **売上向上** (revenue_growth) | [RT-10](patterns/rt-runtime/rt10-event-driven-orchestrator.md)・[KM-3](patterns/km-knowledge/km3-canonical-object-knowledge-graph.md)・[EX-4](patterns/ex-experience/ex4-trust-value-ux.md)・[IN-2](patterns/in-integration/in2-saas-connector-adapter.md) | [Sales Agent](integration/departments/sales.md) |
| **業務自動化** (automation) | [RT-7](patterns/rt-runtime/rt7-enterprise-saga.md)・[RT-10](patterns/rt-runtime/rt10-event-driven-orchestrator.md)・[RT-8](patterns/rt-runtime/rt8-durable-workflow.md)・[RT-9](patterns/rt-runtime/rt9-work-queue-agent.md) | [HR Agent](integration/departments/hr.md)・[CS Agent](integration/departments/customer-support.md) |
| **従業員効率** (employee_efficiency) | [KM-1](patterns/km-knowledge/km1-access-controlled-rag.md)・[KM-2](patterns/km-knowledge/km2-context-mesh.md)・[EX-2](patterns/ex-experience/ex2-embedded-vs-portal.md)・[KM-4](patterns/km-knowledge/km4-scoped-memory-hierarchy.md) | [Engineering Agent](integration/departments/engineering.md) |
| **経営判断加速** (executive_decision) | [KM-3](patterns/km-knowledge/km3-canonical-object-knowledge-graph.md)・[KM-2](patterns/km-knowledge/km2-context-mesh.md)・[KM-6](patterns/km-knowledge/km6-dlp-redaction-boundary.md)・[GV-10](patterns/gv-governance/gv10-two-layer-value-measurement.md) | [Executive Agent](integration/departments/executive.md) |
| **顧客価値** (customer_value) | [EX-3](patterns/ex-experience/ex3-channel-agnostic-frontdoor.md)・[RT-3](patterns/rt-runtime/rt3-risk-tiered-autonomy.md)・[KM-1](patterns/km-knowledge/km1-access-controlled-rag.md) | [CS Agent](integration/departments/customer-support.md) |
| **監査・コンプライアンス** (audit_compliance) | [ID-2](patterns/id-identity/id2-identity-federation-obo.md)・[OB-2](patterns/ob-observability/ob2-unified-audit-lineage.md)・[ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md)・[GV-4](patterns/gv-governance/gv4-industry-policy-pack.md) | 全部門共通 |
| **プロジェクト生産性** (project_productivity) | [RT-11](patterns/rt-runtime/rt11-project-digital-twin.md)・[RT-2](patterns/rt-runtime/rt2-raci-multi-agent.md)・[KM-4](patterns/km-knowledge/km4-scoped-memory-hierarchy.md) | [Engineering Agent](integration/departments/engineering.md) |

## 設計の根本方針

> **価値を生むために動かし、壊さないために統べる。** AIエージェントを企業に導入するとは、LLMを業務システムにつなぐことではありません。企業のID・権限・責任・データ・プロセス・監査・組織構造の中に新しい実行主体を安全に参加させ、受注率向上・業務自動化・生産性改善・意思決定加速という価値を引き出す——それが本質といえます。決定論的な権限・組織・監査の統制基盤の上で、確率的な知能が企業価値を生み出します。安全は土台であり、価値が目的です。
