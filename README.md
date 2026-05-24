# エンタープライズAIエージェント・アーキテクチャ・リファレンス

数万人規模・多様な既存SaaS・厳格な権限管理・階層的組織を前提に、AIエージェントをエンタープライズへ安全に組み込むためのアーキテクチャパターン集（7面・45パターン）。MkDocs（Material）で生成し GitHub Pages で公開する。

## クイックスタート

```bash
uv sync               # 依存関係のインストール
uv run mkdocs serve   # http://127.0.0.1:8000
uv run mkdocs build --strict # 本番同等ビルド（警告ゼロが品質ゲート）
```

## ドキュメントの役割

- **[PROJECT.md](PROJECT.md)** … 何を・なぜ・どの順で作るか（仕様・計画・全45パターン一覧・完了の定義）。
- **[CLAUDE.md](CLAUDE.md)** … Claude Code 向けの作業マニュアル（コマンド・執筆規約・禁止事項）。
- **`reference/source-unified-enterprise.md`** … 全ページの一次ソース（非公開素材）。

## 公開（GitHub Pages）

1. GitHub にリポジトリを作成し push（デフォルトブランチ `main`）。
2. `mkdocs.yml` の `site_url` / `repo_url` / `repo_name` の `USERNAME` を実値に変更。
3. `main` への push で `.github/workflows/deploy.yml` が `gh-pages` ブランチへ自動公開。
4. リポジトリ設定 → Pages → Source を **`gh-pages` ブランチ**に設定。

## 構成（7面）

```text
面1 EX 体験・ゲートウェイ / 面2 GV 制御・ガバナンス / 面3 ID アイデンティティ・信頼(最難関)
面4 RT 実行・オーケストレーション / 面5 KM 知識・メモリ / 面6 IN 統合・ツール / 面7 OB 観測・評価・監査
```

詳細なディレクトリ構成・パターン一覧は [PROJECT.md](PROJECT.md) を参照。
