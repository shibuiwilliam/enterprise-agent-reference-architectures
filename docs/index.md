---
title: "ホーム"
description: "数万人規模の従業員・顧客と多様な既存SaaSを前提に、AIエージェントをエンタープライズへ安全に組み込むためのアーキテクチャパターン集。"
---

# エンタープライズAIエージェント・アーキテクチャ・リファレンス

エンタープライズにAIエージェントを組み込む中心課題は「**AIを賢くすること**」ではなく、「**企業の既存のID・権限・責任・業務プロセス・監査・データ境界・組織構造の中に、新しい実行主体を安全に参加させ、売上・生産性・意思決定の向上という企業価値を引き出すこと**」である。安全に参加させることは前提条件であり、目的は企業価値の向上である。

本サイトは、数万人規模・多様な既存SaaS（Salesforce / ServiceNow / Workday / Okta / Slack / Box / Jira / Zendesk / Shopify / バクラク / Sansan ほか）・厳格な権限管理・階層的組織を前提に、7面・45パターンを共通スキーマで整理した実務リファレンスである。

!!! note "「45パターン」の内訳"
    本サイトのコンテンツは以下の3層で構成される。**コアパターン 45**（7面：体験3＋ガバナンス10＋アイデンティティ8＋ランタイム11＋知識7＋統合4＋観測2）が設計の本体であり、**選定基準 21**（程度9＋トレードオフ12）がパラメータ調整と二者択一の判断軸を、**統合・リファレンス構成**（依存チェーン・組み合わせレシピ・部門別適用例・成熟度ロードマップ・標準構成図）が導入順序と組み合わせ方を補完する。

## 本サイトの構成

<div class="grid cards" markdown>

- :material-flag-outline: **[はじめに](overview/agenda.md)**

    中心命題・エージェント分類学・組織グラフ・7面アーキテクチャ・標準整合。

- :material-shape-outline: **[パターンカタログ](patterns/index.md)**

    7面・45パターンを共通スキーマで記述。

- :material-tune-variant: **[「程度」の選定基準](selection/degree/index.md)**

    自律度ティア・予算・ログ三層分離・ガードレール強度など連続量の決め方。

- :material-scale-balance: **[「相反する仕組み」の選定基準](selection/tradeoff/index.md)**

    OBO/SA・中央レイク/Mesh・Copilot/Autopilot など二者択一の判断軸。

- :material-puzzle-outline: **[統合と組み合わせ方](integration/dependency-chain.md)**

    依存関係・横断軸・組み合わせレシピ・部門別適用例・リファレンスアーキテクチャ。

- :material-chart-line: **[価値設計（成果KPI・導入順序・ユースケース選定）](integration/departments/index.md)**

    各部門の成果KPIマッピング・[価値成熟度ロードマップ](integration/value-maturity-roadmap.md)・[ユースケース選定ガイド](integration/usecase-selection-guide.md)・[定着・アダプション](integration/adoption.md)・[AI投資ポートフォリオ](integration/portfolio.md)。

</div>

## 価値とROI（なぜAIエージェントを導入するのか）

エンタープライズAIエージェントが創出する企業価値は以下の5軸に集約される。

| 価値軸 | 効果の例 | 関連ページ |
|---|---|---|
| **売上・利益改善** | 受注率向上・アップセル示唆・失注予兆検知 | [Sales Agent](integration/departments/sales.md)・[GV-10 価値計測（3層）](patterns/gv-governance/gv10-two-layer-value-measurement.md) |
| **業務自動化** | バックオフィスの端到端処理・定型業務のゼロタッチ化 | [組み合わせレシピ](integration/recipe.md)・[RT-10 イベント駆動](patterns/rt-runtime/rt10-event-driven-orchestrator.md) |
| **プロジェクト生産性** | リードタイム短縮・ボトルネック検知・情報共有の即時化 | [RT-11 デジタルツイン](patterns/rt-runtime/rt11-project-digital-twin.md)・[Engineering Agent](integration/departments/engineering.md) |
| **従業員効率** | 情報検索・ドラフト生成・トリアージの自動化 | [KM-1 権限認識RAG](patterns/km-knowledge/km1-access-controlled-rag.md)・[定着・アダプション](integration/adoption.md) |
| **経営判断の加速** | 全社KPI横断・シナリオ分析・リスク早期察知 | [Executive Agent](integration/departments/executive.md)・[AI投資ポートフォリオ](integration/portfolio.md) |

!!! tip "クイックウィン：90日で最初のROI"
    読み取り専用・低リスク・高頻度のユースケース（社内ナレッジ検索・議事録要約）から始め、最初の90日で経営に報告可能なROIを実証する。詳細は[組み合わせレシピの価値早期実現トラック](integration/recipe.md)を参照。

## 設計の根本方針

> AIエージェントを企業に導入するとは、LLMを業務システムにつなぐことではなく、企業のID・権限・責任・データ・プロセス・監査・組織構造の中に、新しい実行主体を安全に参加させ、その上で売上・生産性・意思決定の向上という価値を引き出すことである。確率的な知能を、決定論的な権限・組織・監査の檻の中に閉じ込めたとき、初めて数万人規模の本番に耐えるエンタープライズAIエージェントが成立し、安全な檻の中で解き放たれた知能が企業価値を生み出す。

