---
id: P33
slug: DEPARTMENT-SCOPED-AGENT
title: "P33 · DEPARTMENT-SCOPED-AGENT — 部署スコープのエージェント"
category: 組織
audience: employee
maturity: 標準
related: [P14, P16, P36]
status: done
---

# P33 · DEPARTMENT-SCOPED-AGENT — 部署スコープのエージェント

!!! abstract "一言で"
    組織の Role & Responsibility に沿って、部署/ドメインごとに専門エージェントを定義するパターン。営業・IT・人事・法務・開発など、各部署固有の知識・ツール・権限・トーンを持つエージェントを配置し、組織の自然な境界に合わせた権限・責任の分離を実現する。

## 解決する問題

- **権限/知識の自然な境界**: 部署ごとに異なるデータアクセス権限・業務知識を反映できない。
- **説明責任の明確化**: エージェントの所有者（部署長）と責任範囲が不明確。
- **部署特有の文脈**: 営業用語・IT用語・人事ポリシーなど部署固有の知識が混在する。

## 選定条件

**採用する場合（When to use）**

- 部署ごとに業務・ツール・規制が大きく異なる。
- 部署ごとに業務・ツール・規制が大きく異なる大企業。

**採用しない場合（When NOT）**

- 横断業務が大半で部署境界が意味をなさない組織。

## 構造

- 組織グラフと権限をSCIM/HRIS（Workday / Okta）から同期し、部署メンバーシップに基づくスコープを動的に維持する（[P14](../memory/p14-semantic-layer.md)）。
- 各部署エージェントの利用可能ツールとデータ範囲を部署単位で制約する。
- スーパーバイザ/ルーター（[P16](../orchestration/p16-supervisor-router.md)）が入口で意図を分類し、適切な部署エージェントへ振り分ける。
- エージェントのライフサイクルは組織変更に追従する（[P36](../governance/p36-digital-employee-lifecycle.md)）。

## ユースケース

- 営業部エージェント（Salesforce・Slack連携、商談データへのアクセス権限）、IT部エージェント（ServiceNow・Jira連携、インフラデータへの権限）、人事部エージェント（Workday連携、給与・人事データへの限定権限）をそれぞれ独立して運用する。
- Slackの全社AIハブで「有給の残日数を教えて」→人事エージェント、「VPNが繋がらない」→ITエージェントへ自動振り分け。

## 実装メモ

SCIM同期、HRIS連携（Workday / BambooHR）、組織グラフ（[P14](../memory/p14-semantic-layer.md)）、スーパーバイザ/ルーター（[P16](../orchestration/p16-supervisor-router.md)）。

## 関連パターン

**カテゴリ**: 組織 ／ **対象**: 従業員 ／ **成熟度**: 標準

- [P14 セマンティックレイヤー](../memory/p14-semantic-layer.md)
- [P16 スーパーバイザ/ルーター](../orchestration/p16-supervisor-router.md)
- [P36 デジタル従業員ライフサイクル](../governance/p36-digital-employee-lifecycle.md)
