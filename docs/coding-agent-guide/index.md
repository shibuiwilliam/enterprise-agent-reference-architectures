---
title: "コーディングエージェント向けガイド"
description: "コーディングエージェントが本リファレンスを活用してエンタープライズAIエージェントのアーキテクチャを提案するためのガイド。"
status: done
---

# コーディングエージェント向けガイド

本章は、コーディングエージェント（GitHub Copilot、Claude Code、Cursor 等）が本リファレンスを読み込み、エンタープライズAIエージェントのアーキテクチャを設計・提案する際の手引きとなります。

## 本サイトの読み方

コーディングエージェントは以下の順序で本サイトを参照するとよいでしょう。

1. **リポジトリルートの `agents.md`** を最初に読みます。推論手順と出力テンプレートの全体像を把握します。
2. **`docs/_machine/index.json`** からスキーマバージョンと各リソースのパスを取得します。
3. 要件に応じて `patterns.json`・`decisions.json`・`value-loop.json`・`departments.json` を参照します。
4. 詳細が必要な場合のみ、個別のマークダウンページを読みます。

## 推論手順：要件→候補パターン→アーキテクチャ提案

### Step 1：要件の構造化

ユーザーの要件から以下を抽出します。

| 抽出項目 | 例 |
|---|---|
| 目的（value_drivers） | revenue_growth, automation |
| 制約（規制・機密度） | 金融業（GV-4 適用）、機密レベル高 |
| 現行SaaS | Salesforce, Workday, Slack |
| 許容自律度 | Copilot（TO-5） |
| 組織規模 | 5,000名、3事業部 |

### Step 2：意思決定基準の評価

`decisions.json` から関連する DC/TO を特定し、各オプションの pick_when 条件と要件を照合します。

### Step 3：パターンの選定と依存解決

選択したオプションが要求する patterns を `patterns.json` から取得し、prerequisites を再帰的に解決します。

### Step 4：組み合わせの構成

- 最小安全ベースライン（ID-1 + ID-6 + GV-1 + OB-2）
- 30〜60日クイックウィン（読み取り専用ユースケース）
- 拡大段（書き込み権限付与、マルチエージェント化）
- 定着・計測（GV-10 + adoption）
- 投資判断（portfolio）

### Step 5：出力の生成

`agents.md` に定義された出力テンプレートに従い、人間に提示するアーキテクチャ提案を生成します。

## 出力テンプレート

提案は以下の構造で出力します。

| セクション | 内容 |
|---|---|
| 目的とKPI | 価値ドライバと目標指標 |
| 採用パターン（plane別） | 7面それぞれの採用パターン |
| 意思決定の根拠 | DC/TO の選択とその理由 |
| 最小安全ベースライン＋クイックウィン | MVP構成と初期価値 |
| 価値の階段 | 可視化→分析→実行の3段階 |
| 定着・計測・投資 | 運用フェーズの設計 |
| リスクと未解決事項 | 残るトレードオフ |

## 機械可読データの参照方法

`docs/_machine/` 配下の JSON ファイルを直接パースして利用します。

| ファイル | 用途 |
|---|---|
| `index.json` | エントリポイント、スキーマバージョン確認 |
| `patterns.json` | パターン検索・依存解決 |
| `decisions.json` | 意思決定基準の評価 |
| `value-loop.json` | 価値ループのナビゲーション |
| `departments.json` | 部門事例の参照 |

## 価値ドライバ語彙（統一タグ）

| タグ | 意味 |
|---|---|
| employee_efficiency | 従業員の業務効率化 |
| decision_quality | 意思決定の質と速度向上 |
| automation | 業務プロセスの自動化 |
| revenue_growth | 売上・利益の成長 |
| customer_value | 顧客体験・満足度向上 |
| audit_compliance | 監査・コンプライアンスの確保 |
| executive_decision | 経営判断の加速 |
| project_productivity | プロジェクト生産性向上 |

## 関連ページ

- [価値ユースケース選定ガイド](../integration/usecase-selection-guide.md)
- [組み合わせレシピ](../integration/recipe.md)
- [定着・アダプション](../integration/adoption.md)
- [GV-10 三層価値計測](../patterns/gv-governance/gv10-two-layer-value-measurement.md)
- [意思決定の手引き](../decisions/decision-guide.md)
