---
title: "ホーム"
description: "数万人規模の従業員・顧客と多様な既存SaaSを前提に、AIエージェントをエンタープライズへ安全に組み込むためのアーキテクチャパターン集。"
---

# エンタープライズAIエージェント・アーキテクチャ・リファレンス

エンタープライズにAIエージェントを組み込む中心課題は「**AIを賢くすること**」ではなく、「**企業の既存のID・権限・責任・業務プロセス・監査・データ境界・組織構造の中に、新しい実行主体を安全に参加させること**」である。

本サイトは、数万人規模・多様な既存SaaS（Salesforce / ServiceNow / Workday / Okta / Slack / Box / Jira / Zendesk / Shopify / バクラク / Sansan ほか）・厳格な権限管理・階層的組織を前提に、7面・45パターンを共通スキーマで整理した実務リファレンスである。

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

- :material-puzzle-outline: **[統合と組み合わせ方](integration/dependencies.md)**

    依存関係・組み合わせレシピ・部門別適用例・ロードマップ・設計原則。

</div>

## 設計の根本方針

> AIエージェントを企業に導入するとは、LLMを業務システムにつなぐことではなく、企業のID・権限・責任・データ・プロセス・監査・組織構造の中に、新しい実行主体を安全に参加させることである。確率的な知能を、決定論的な権限・組織・監査の檻の中に閉じ込めたとき、初めて数万人規模の本番に耐えるエンタープライズAIエージェントが成立する。

!!! info "本サイトの執筆について"
    各ページは `reference/source-unified-enterprise.md` を一次ソースに Claude Code で執筆する。執筆手順は `CLAUDE.md`、全体計画は `PROJECT.md` を参照。
