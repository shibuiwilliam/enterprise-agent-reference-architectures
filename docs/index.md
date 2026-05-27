---
title: "ホーム"
description: "数万人規模の従業員・顧客と多様な既存SaaSを前提に、AIエージェントをエンタープライズへ安全に組み込むためのアーキテクチャパターン集。"
---

# エンタープライズAIエージェント・アーキテクチャ・リファレンス

エンタープライズにAIエージェントを組み込む中心課題は「**AIを賢くすること**」ではなく、「**価値を生むために動かし、壊さないために統べる**」ことにある。企業の既存のID・権限・責任・業務プロセス・監査・データ境界・組織構造の中に新しい実行主体を安全に参加させ、受注率向上・業務自動化・生産性改善・意思決定加速という**企業価値を引き出す**——安全はその土台であり、目的はあくまで企業価値の向上にある。

本サイトは、数万人規模・多様な既存SaaS（Salesforce / ServiceNow / Workday / Okta / Slack / Box / Jira / Zendesk / Shopify / バクラク / Sansan ほか）・厳格な権限管理・階層的組織を前提に設計された実務リファレンスである。**45パターン（安全に動かす型）**と**価値運用ページ群（価値を出す型）**の二本立てで構成される。

!!! note "本サイトの二重構造"
    **45パターン**（7面：体験3＋ガバナンス10＋アイデンティティ8＋ランタイム11＋知識7＋統合4＋観測2）がエージェントを**安全に動かす設計の型**を、**選定基準 21**（程度9＋トレードオフ12）が調整と判断軸を提供する。これに加え、**価値運用ページ群**（[価値成熟度ロードマップ](integration/value-maturity-roadmap.md)・[ユースケース選定ガイド](integration/usecase-selection-guide.md)・[GV-10 三層価値計測](patterns/gv-governance/gv10-two-layer-value-measurement.md)・[定着・アダプション](integration/adoption.md)・[AI投資ポートフォリオ](integration/portfolio.md)）が**価値を出す運用の型**を提供する。45パターンで安全を確保し、価値運用ページ群で成果を出す——この二重構造が本サイトの設計思想である。

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

- :material-chart-line: **[価値運用ページ群（価値を出す型）](integration/value-maturity-roadmap.md)**

    [価値成熟度ロードマップ](integration/value-maturity-roadmap.md)（導入順序）・[ユースケース選定ガイド](integration/usecase-selection-guide.md)（初期ユースケースの選び方）・[GV-10 三層価値計測](patterns/gv-governance/gv10-two-layer-value-measurement.md)（ROI計測）・[定着・アダプション](integration/adoption.md)（チェンジマネジメント）・[AI投資ポートフォリオ](integration/portfolio.md)（再投資判断）・[部門別適用例](integration/departments/index.md)（成果KPIマッピング）。

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

## 価値ループ：創出→計測→定着→再投資

45パターンが安全な実行基盤を提供し、その上で価値が4ステップを循環する。このループを回し続けることが、企業価値向上の実体である。

```mermaid
flowchart LR
    subgraph ValueLoop["価値ループ"]
        CREATE["① 価値創出<br/>部門別ユースケース実行"]
        MEASURE["② 計測<br/>GV-10 三層価値計測"]
        ADOPT["③ 定着<br/>チェンジマネジメント"]
        REINVEST["④ 再投資<br/>AI投資ポートフォリオ"]
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
| ① 価値創出 | 部門別エージェントが成果KPIを動かす | [部門別適用例](integration/departments/index.md)・[組み合わせレシピ](integration/recipe.md) |
| ② 計測 | 定着率→生産性→経営KPIの3層で因果を追跡 | [GV-10 Three-Layer Value Measurement](patterns/gv-governance/gv10-two-layer-value-measurement.md) |
| ③ 定着 | 利用率を引き上げ、ROIの分母を確保する | [定着・アダプション](integration/adoption.md) |
| ④ 再投資 | 計測結果に基づき拡大・改善・撤退を判断 | [AI投資ポートフォリオ](integration/portfolio.md)・[ユースケース選定ガイド](integration/usecase-selection-guide.md) |

## 設計の根本方針

> **価値を生むために動かし、壊さないために統べる。** AIエージェントを企業に導入するとは、LLMを業務システムにつなぐことではない。企業のID・権限・責任・データ・プロセス・監査・組織構造の中に新しい実行主体を安全に参加させ、受注率向上・業務自動化・生産性改善・意思決定加速という価値を引き出すことである。決定論的な権限・組織・監査の統制基盤の上で、確率的な知能が企業価値を生む——安全は土台であり、価値が目的だ。

