# PROJECT.md — エンタープライズAIエージェント アーキテクチャパターン ドキュメント

## 1. このプロジェクトは何か

数万人規模の従業員・顧客と、多様なSaaS（Salesforce / ServiceNow / Workday / Okta / Slack /
M365 / Box / Sansan / Google Workspace / AWS / Linear / Notion / Jira / Zendesk / Shopify /
Auth0 等）および独自開発システムが併存する企業に対し、**AIエージェントを本番システムへ
組み込むためのアーキテクチャパターン・カタログ（全30パターン）**を執筆・公開する。

- **想定読者は2種類**：(1) アーキテクチャを学び判断する**人間**、(2) 要件を受け取り、
  このカタログを引用しながら設計し人間に提案する**コーディングエージェント**。
- **公開方法**：MkDocs（Material テーマ）でビルドし、GitHub Pages で公開する。
- **執筆方法**：Claude Code が `docs/` 配下の各ページを `CLAUDE.md` の規約に従って執筆する。

## 2. ゴールと完成の定義（Definition of Done）

各パターンページが以下をすべて満たしたとき `status: done` とする。

- フロントマター（`id` / `slug` / `title` / `category` / `audience` / `maturity` / `related` / `status`）が正しい。
- 固定フィールドがすべて埋まっている：**トリガ / 概要 / 設計 / 解決する課題 / ユースケース / 向き・不向き / 要素技術**。
- トリガが「要件と機械照合できるIF条件」になっている（コーディングエージェントが選定に使えること）。
- 該当する場合、**程度の判断（⚠️ warning admonition）** と **相反する仕組み（⚖️ note admonition）** を含む。
- 関連パターンへの相互リンクが相対パスで張られている。
- 前提企業のSaaSに即した具体例が入っている。
- `mkdocs build --strict` がエラー・警告なしで通る。

サイト全体としては、`mkdocs build --strict` がパスし、GitHub Pages で全ページが閲覧でき、
ナビゲーションが `mkdocs.yml` と一致していることをもって公開可能とみなす。

## 3. ディレクトリ構成

```
.
├── PROJECT.md                  # 本ファイル（プロジェクト定義・マニフェスト）
├── CLAUDE.md                   # Claude Code 向けの執筆・運用ガイド（規約の正本）
├── README.md                   # クイックスタート
├── mkdocs.yml                  # サイト設定・ナビゲーション
├── pyproject.toml              # 依存管理（uv）
├── .gitignore
├── .github/workflows/deploy.yml  # GitHub Pages 自動デプロイ
└── docs/
    ├── index.md                # ホーム：4つの摩擦・横断原則・5つの問い
    ├── usage/                  # コーディングエージェント向けの使い方
    │   ├── design-protocol.md      # 設計プロトコル（8ステップ）
    │   ├── pattern-schema.md        # パターン記述フォーマット規約
    │   └── proposal-template.md     # 提案アウトプット・テンプレート
    ├── patterns/
    │   ├── index.md            # パターン索引（機械可読の一覧表）
    │   ├── trust-boundary/     # P01–P02
    │   ├── integration/        # P03–P07
    │   ├── identity/           # P08–P11
    │   ├── memory/             # P12–P14
    │   ├── orchestration/      # P15–P18
    │   ├── determinism/        # P20–P21
    │   ├── reliability/        # P22–P27
    │   ├── freshness/          # P31
    │   ├── organization/       # P33–P35
    │   ├── governance/         # P36–P37
    │   └── regulation/         # P40
    ├── selection/
    │   ├── degree-criteria.md      # 「程度」の選定基準（ルックアップ表）
    │   └── tension-criteria.md     # 「相反する仕組み」の選定基準（ルックアップ表）
    └── reference-architecture.md   # 層構造・導入順序・まとめ
```

1パターン＝1ファイル。Git差分が綺麗になり、RAGでの分割取得にも耐え、Claude Code が
1パターン単位で並行・段階的に執筆できる。

## 4. コンテンツ・マニフェスト（進捗チェックリスト）

`status` フロントマターで管理する。`draft` → `review` → `done`。

### 共通ページ
- [x] `docs/index.md`（ホーム）
- [x] `docs/usage/design-protocol.md`
- [x] `docs/usage/pattern-schema.md`
- [x] `docs/usage/proposal-template.md`
- [x] `docs/patterns/index.md`（索引表）
- [x] `docs/selection/degree-criteria.md`
- [x] `docs/selection/tension-criteria.md`
- [x] `docs/reference-architecture.md`

### パターン（執筆対象）
凡例：✅=done / 🟡=review / ⬜=draft（スタブ）

| ID | パターン | カテゴリ | 状態 |
|----|---------|---------|------|
| P01 | 信頼境界の二層分離 | 信頼境界 | ✅（執筆例） |
| P02 | マルチテナント分離 | 信頼境界 | ✅（執筆例） |
| P03 | AIエージェント・ゲートウェイ | 統合 | ⬜ |
| P04 | MCPゲートウェイ | 統合 | ⬜ |
| P06 | エージェント・ハブ | 統合 | ⬜ |
| P07 | イベント駆動エージェント | 統合 | ⬜ |
| P08 | トークン交換(OBO) | ID/認可 | ⬜ |
| P09 | 動的認可(PDP/PBAC) | ID/認可 | ⬜ |
| P10 | コンテキスト・ファイアウォール | ID/認可 | ⬜ |
| P11 | ゼロトラスト/サンドボックス | ID/認可 | ⬜ |
| P12 | 階層化メモリ | メモリ | ⬜ |
| P14 | セマンティックレイヤー | メモリ | ⬜ |
| P15 | シングル vs マルチ | オーケストレーション | ⬜ |
| P16 | スーパーバイザ/ルーター | オーケストレーション | ⬜ |
| P17 | 決定論ワークフロー併用 | オーケストレーション | ⬜ |
| P18 | HITL承認ゲート | オーケストレーション | ⬜ |
| P20 | 二重トラック検証 | 確率→決定論 | ⬜ |
| P21 | 信頼度ゲート棄権 | 確率→決定論 | ⬜ |
| P22 | 非同期ジョブ＋コールバック | 信頼性/運用 | ⬜ |
| P23 | サーキットブレーカ/フォールバック | 信頼性/運用 | ⬜ |
| P24 | セマンティック/プロンプトキャッシュ | 信頼性/運用 | ⬜ |
| P25 | オブザーバビリティ/トレース | 信頼性/運用 | ⬜ |
| P26 | 評価ゲート/カナリア | 信頼性/運用 | ⬜ |
| P27 | コストガバナンス | 信頼性/運用 | ⬜ |
| P31 | CDC駆動の知識鮮度 | 知識鮮度 | ⬜ |
| P33 | 部署スコープのエージェント | 組織 | ⬜ |
| P35 | エージェント・レジストリ | 組織 | ⬜ |
| P36 | デジタル従業員ライフサイクル | ガバナンス | ⬜ |
| P37 | プロンプト・サプライチェーン | ガバナンス | ⬜ |
| P40 | フィードバックループ | 規制/改善 | ⬜ |

## 5. 推奨される執筆の進め方（Claude Code）

1. `CLAUDE.md` を読み、パターン記述フォーマットと禁止事項を把握する。
2. P01・P02（執筆済みの正本サンプル）を読み、トーン・粒度・admonitionの使い方を真似る。
3. カテゴリ単位で執筆する（例：まず `integration/` の P03–P07）。1パターン＝1コミット。
4. 各ページ完成後に `mkdocs build --strict` を実行し、警告ゼロを確認する。
5. 相互参照（`related`）のリンク先が実在することを確認する。
6. `status` を `done` に更新し、本マニフェストの状態列も更新する。

## 6. 公開（GitHub Pages）

- ローカル確認：`uv sync && uv run mkdocs serve` → http://127.0.0.1:8000
- 本番ビルド検証：`uv run mkdocs build --strict`
- デプロイ：`main` に push すると `.github/workflows/deploy.yml` が `gh-pages` ブランチへ公開。
- **初回のみ** GitHub の `Settings > Pages` で「Deploy from a branch → `gh-pages` / `(root)`」を設定。
- `mkdocs.yml` の `site_url` / `repo_url` を実際のリポジトリに合わせて書き換えること。
