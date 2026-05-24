#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/claude/ent-agent-docs
YML="$ROOT/mkdocs.yml"

declare -A CATNAME=(
[ex-experience]="面1 体験・ゲートウェイ" [gv-governance]="面2 制御・ガバナンス" [id-identity]="面3 アイデンティティ・信頼"
[rt-runtime]="面4 実行・オーケストレーション" [km-knowledge]="面5 知識・メモリ" [in-integration]="面6 統合・ツール"
[ob-observability]="面7 観測・評価・監査"
)
ORDER=(ex-experience gv-governance id-identity rt-runtime km-knowledge in-integration ob-observability)
get_title() { grep -m1 '^title:' "$1" | sed -E 's/^title: *"?//; s/"?$//'; }

cat > "$YML" << 'HEAD'
site_name: エンタープライズAIエージェント・アーキテクチャ・リファレンス
site_description: 数万人規模・多様な既存SaaS・厳格な権限管理・階層的組織を前提とした、AIエージェントのエンタープライズ組み込みアーキテクチャパターン集
site_author: ""
# GitHub Pages 公開時に正しいパスになるよう、実リポジトリに合わせて書き換える
site_url: https://USERNAME.github.io/ent-agent-docs/
repo_url: https://github.com/USERNAME/ent-agent-docs
repo_name: USERNAME/ent-agent-docs
edit_uri: edit/main/docs/

theme:
  name: material
  language: ja
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: teal
      accent: teal
      toggle:
        icon: material/weather-night
        name: ダークモードへ
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: teal
      accent: teal
      toggle:
        icon: material/weather-sunny
        name: ライトモードへ
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - toc.follow
    - content.code.copy
    - search.suggest
    - search.highlight

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - footnotes
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

plugins:
  - search:
      lang: ja

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/USERNAME/ent-agent-docs

# nav は scripts/build_nav.sh で再生成できる（CLAUDE.md 参照）
nav:
  - ホーム: index.md
  - はじめに:
      - 中心命題・分類学・組織グラフ・7面: overview/agenda.md
      - 項目設計と面分類: overview/schema.md
  - パターンカタログ:
      - 概要: patterns/index.md
HEAD

for dir in "${ORDER[@]}"; do
  echo "      - ${CATNAME[$dir]}:" >> "$YML"
  echo "          - patterns/$dir/index.md" >> "$YML"
  for p in "$ROOT/docs/patterns/$dir"/*.md; do
    base=$(basename "$p")
    [ "$base" = "index.md" ] && continue
    t=$(get_title "$p")
    echo "          - \"$t\": patterns/$dir/$base" >> "$YML"
  done
done

cat >> "$YML" << 'TAIL'
  - 選定基準:
      - 「程度」の選定基準: selection/degree-criteria.md
      - 「相反する仕組み」の選定基準: selection/tradeoffs.md
  - 統合と組み合わせ方:
      - 依存関係と組み合わせレシピ: integration/dependencies.md
      - 部門別 適用例: integration/department-examples.md
      - 成熟度ロードマップ: integration/roadmap.md
      - リファレンスアーキテクチャ: integration/reference-architecture.md
      - 設計原則: integration/principles.md
TAIL
echo "mkdocs.yml written ($(wc -l < "$YML") lines)"
