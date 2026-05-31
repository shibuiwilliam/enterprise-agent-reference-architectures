# エンタープライズAIエージェント アーキテクチャパターン

数万人規模の従業員・顧客と多様なSaaS・独自システムが併存する企業に、AIエージェントを
本番システムへ組み込むためのアーキテクチャパターン集（全30パターン）です。
**人間とコーディングエージェントの双方**を読者とし、MkDocs（Material）＋ GitHub Pages で公開します。

## クイックスタート

```bash
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000 でプレビュー
mkdocs build --strict # 公開前チェック
```

## ドキュメントを書く

- 執筆・運用の規約は **[CLAUDE.md](./CLAUDE.md)**（正本）。
- プロジェクト定義・進捗マニフェストは **[PROJECT.md](./PROJECT.md)**。
- 1パターン＝1ファイル（`docs/patterns/<category>/<id>-<slug>.md`）。
- 正本サンプル：`docs/patterns/trust-boundary/p01-trust-boundary-split.md`、`p02-...md`。

## 公開（GitHub Pages）

1. `mkdocs.yml` の `site_url` / `repo_url` を自分のリポジトリに合わせる。
2. `main` に push すると GitHub Actions（`.github/workflows/deploy.yml`）が `gh-pages` へ公開。
3. 初回のみ `Settings > Pages` で「Deploy from a branch → `gh-pages` / `(root)`」を設定。
