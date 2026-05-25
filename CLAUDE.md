# CLAUDE.md

Claude Code 向けの作業マニュアル。**何を作るか**は `PROJECT.md`、本書は**どう作業するか**を定める。作業前に毎回、対象ページの一次ソース節（`reference/source-unified-enterprise.md`）を読むこと。

---

## リポジトリ概要

MkDocs（Material テーマ）製のドキュメントサイト。`docs/` を編集し、GitHub Pages へ自動公開する。中身はエンタープライズAIエージェントのアーキテクチャパターン集（7面・45パターン）。公開対象は `docs/` のみ。`reference/` は執筆素材で**公開しない・編集しない**。

中心命題：「AIを賢くすること」ではなく「企業のID・権限・責任・プロセス・監査・組織構造の中に実行主体を安全に参加させること」。この視点を全ページで貫く。

## 環境セットアップ

```bash
uv sync
```

## よく使うコマンド

```bash
uv run mkdocs serve              # ローカルプレビュー（http://127.0.0.1:8000、ホットリロード）
uv run mkdocs build --strict     # 本番同等ビルド。リンク切れ・nav不整合を警告でなくエラーにする
bash scripts/build_nav.sh        # docs ツリーから mkdocs.yml の nav を再生成
```

**コミット前に必ず `mkdocs build --strict` を通すこと。** 警告ゼロが品質ゲート。

## 執筆ワークフロー（1パターン＝1作業単位）

1. `PROJECT.md` のパターン一覧から対象ID（例 `ID-2`）を選ぶ。
2. **一次ソースを読む**：`reference/source-unified-enterprise.md` の該当節（`ID-2`）。
3. 対象ファイル（例 `docs/patterns/id-identity/id2-identity-federation-obo.md`）を開く。
4. 共通スキーマの全7節を、ソースの主旨に沿って埋める（下記規約に従う）。
5. フロントマターを更新：`description` を1文記入、`status: draft` → `status: done`。
6. `## 関連パターン` に依存・併用パターンへの**相対リンク**を張る。
7. `mkdocs build --strict` を通す。
8. 1パターン＝1コミット（粒度を小さく保つ）。

## 執筆規約

### 文体・トーン
- 常体（だ・である）で統一。簡潔・技術的に。一文を短く。
- 主観的な優劣評価や誇張をしない。トレードオフは中立に併記する。
- ソースに無い事実・固有名を勝手に足さない。足す場合は出典付き・断定を避ける。

### 構造（パターンページ）
- 見出しは `PROJECT.md` 4.1 の8節を**この順序・この名称で固定**。節を増減しない。
- 各節は基本プローズ。箇条書きは要素列挙（要素技術・SaaS等）に限定し、各項目は短く。
- 「向き／不向き」は対になるよう具体条件で書く。
- 「落とし穴／選定の勘所」は実際に起きるアンチパターンを具体的に書く（例：「万能サービスアカウント1個で全SaaSを叩く」）。

### フロントマター
```yaml
---
title: "ID-2 Identity Federation & On-Behalf-Of（OBO委譲）"  # nav と一致させる
description: "依頼者本人の権限に縮退した委譲トークンで下流SaaSを呼び、権限を忠実に伝播するパターン。"
status: done   # 執筆完了時に draft から変更
---
```

### 相互リンク
- 同面内：`[ID-4 権限忠実アクセス](id4-permission-mirror-least-of.md)`
- 別面：`[KM-1 権限認識RAG](../km-knowledge/km1-access-controlled-rag.md)`
- リンク先は**ファイルパス（.md 付き）**で書く。`--strict` がパスを検証する。

### 図・表（Material 機能）
- フロー・構成・状態遷移・**認可シーケンス**は mermaid を使う。特に ID-2（OBO/トークン交換）、ID-6（PDP/PEP）、RT-7（Saga）、RT-10（イベント駆動）はシーケンス/フロー図を推奨：
  ````markdown
  ```mermaid
  sequenceDiagram
    participant U as User
    participant GW as Agent Gateway
    participant SF as Salesforce
    U->>GW: 依頼 (IDトークン)
    GW->>GW: Token Exchange (RFC 8693) で OBO トークン発行
    GW->>SF: 本人権限でAPI呼び出し
  ```
  ````
- 比較・対照（OBO vs SA、中央レイク vs Mesh 等）は Markdown テーブル。
- 補足・注意は admonition：`!!! note` / `!!! warning` / `!!! tip`。セキュリティ上の重大注意は `!!! danger`。
- 選択肢の出し分けは `=== "タブ名"`（pymdownx.tabbed）。

## ナビゲーション（nav）の扱い

- 新規ページ追加・ファイル名変更時は `mkdocs.yml` の `nav` を更新する。
- ファイルを増減したら **`bash scripts/build_nav.sh`** で nav を再生成するのが安全（titleの取りこぼし・順序ずれを防ぐ）。
- 再生成後は `git diff mkdocs.yml` を確認し、`USERNAME` 等の手編集箇所を壊していないかチェック。

## デプロイ

- `main` への push で `.github/workflows/deploy.yml` が `mkdocs gh-deploy` を実行し、`gh-pages` ブランチへ公開する。
- 初回のみ GitHub リポジトリ設定で **Pages のソースを `gh-pages` ブランチ**に設定する。
- `mkdocs.yml` の `site_url` / `repo_url` / `repo_name` の `USERNAME` を実リポジトリに合わせて書き換える。

## やってはいけないこと（エンタープライズ特有の注意を含む）

- `reference/` の編集・公開（一次ソース／非公開素材）。
- 共通スキーマの節の改変（順序・名称・増減）。
- nav とフロントマター `title` の不一致を残すこと。
- `mkdocs build --strict` の警告を残してコミットすること。
- ソースに無い内容の創作・水増し、特定製品の優劣断定。
- **顧客面と従業員面の境界をまたぐ設計例を書くこと**（ID-1 の原則に反する。両面分離を崩さない）。
- **「プロンプトでセキュリティを守る」と読める記述**（ID-7 の原則に反する。安全保証は実行基盤側）。
- 実在の社内システム名・実データ・実在の個人情報を例に使うこと（架空例で書く）。
- `site/`（ビルド成果物）のコミット（`.gitignore` 済み）。

## 完了チェックリスト（各ページ）

- [ ] 一次ソースの該当節を反映している
- [ ] 7節すべてに内容があり TODO が残っていない
- [ ] `title` が nav と一致、`description` 記入済み、`status: done`
- [ ] 内部リンクが有効（`mkdocs build --strict` が警告なし）
- [ ] 必要箇所に mermaid 図がある（認可・Saga・イベントは特に）
- [ ] 顧客面/従業員面の分離、権限の最小合成、実行基盤での防御という原則に反していない
