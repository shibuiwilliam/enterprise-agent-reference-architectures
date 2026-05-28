# agents.md — Coding Agent Reading Guide

このドキュメントは、AIエージェントを含むエンタープライズシステムのソフトウェアアーキテクチャ提案に使われることを想定する。

## 入口
- 機械可読インデックス： docs/_machine/index.json
- パターン定義：       docs/_machine/patterns.json
- 意思決定基準：       docs/_machine/decisions.json
- 価値ループ：         docs/_machine/value-loop.json
- 部門事例：           docs/_machine/departments.json

## 推論手順（要件→アーキテクチャ提案）

1. 要件から「目的（value_drivers）」「制約（規制・データ機密度・組織規模）」「現行SaaS／レガシー」「許容自律度」を抽出する。
2. value_drivers から候補ユースケースを docs/integration/usecase-selection-guide.md で選ぶ。
3. 関連する DC/TO を docs/_machine/decisions.json で特定し、それぞれのオプションを評価する（pick_when / pros / cons）。
4. 選んだオプションが要求する patterns を docs/_machine/patterns.json から取得し、prerequisites を再帰的に解決する。
5. 組み合わせを「最小安全ベースライン＋クイックウィン」「拡大段」「定着・計測」「投資」の4層で整理し、リファレンスアーキテクチャに当てはめる。
6. 人間への提案は下記の出力テンプレートに従う。

## 出力テンプレート（人間に提示するアーキテクチャ提案の形）

```markdown
# 提案アーキテクチャ：<システム名>

## 目的とKPI
- 価値ドライバ：…
- 目標 KPI（GV-10連携）：…

## 採用パターン（plane別）
- EX: …
- GV: …
- ID: …
- RT: …
- KM: …
- IN: …
- OB: …

## 意思決定の根拠（DC/TO）
| 決定 | 採用オプション | 理由 | 代替案と棄却理由 |
|---|---|---|---|

## 最小安全ベースラインと30〜60日クイックウィン
- ベースライン：…
- クイックウィン候補：…

## 価値の階段
- Step 1 可視化／ Step 2 分析・示唆／ Step 3 実行支援

## 定着・計測・投資配分
- 定着施策：…
- 計測指標：…
- ポートフォリオ位置づけ：…

## リスクと未解決事項
- 残るトレードオフ：…
```

## 機械可読データの参照方法

各 JSON ファイルは以下のスキーマに従う：

- `index.json`：エントリポイント。各リソースのパスとスキーマバージョン。
- `patterns.json`：45パターンの id / plane / summary / applies_when / decision_keys / value_drivers / kpis / prerequisites / related / mvp / cost_orientation。
- `decisions.json`：DC/TO 全21項目の id / title / options / default_recommendation。
- `value-loop.json`：価値ループの6ノードと相互リンク、各ノードが参照するパターン群。
- `departments.json`：部門別事例の value_usecases / kpis / value_ladder / applied_patterns。

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
