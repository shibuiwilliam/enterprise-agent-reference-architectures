# AIエージェント本番組み込み アーキテクチャ・リファレンス

AIエージェントを本番システムへ安全・堅牢・スケーラブルに組み込むためのアーキテクチャパターン集（12カテゴリ・約50パターン）。MkDocs（Material）で生成し GitHub Pages で公開する。

## クイックスタート

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve          # http://127.0.0.1:8000
mkdocs build --strict # 本番同等ビルド（警告ゼロが品質ゲート）
```

## ドキュメントの役割

- **[PROJECT.md](PROJECT.md)** … 何を・なぜ・どの順で作るか（仕様・計画・パターン一覧・完了の定義）。
- **[CLAUDE.md](CLAUDE.md)** … Claude Code 向けの作業マニュアル（コマンド・執筆規約・禁止事項）。
- **`reference/source-unified-reference.md`** … 全ページの一次ソース（非公開素材）。

## 公開（GitHub Pages）

1. GitHub にリポジトリを作成し push（デフォルトブランチ `main`）。
2. `mkdocs.yml` の `site_url` / `repo_url` / `repo_name` の `USERNAME` を実値に変更。
3. `main` への push で `.github/workflows/deploy.yml` が `gh-pages` ブランチへ自動公開。
4. リポジトリ設定 → Pages → Source を **`gh-pages` ブランチ**に設定。

## 構成

```text
docs/        公開ドキュメント（overview / patterns / selection / integration）
reference/   一次ソース（非公開）
scripts/     nav 再生成スクリプト
mkdocs.yml   サイト設定・ナビゲーション
```

詳細なディレクトリ構成は [PROJECT.md](PROJECT.md) を参照。
