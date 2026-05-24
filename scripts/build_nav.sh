#!/usr/bin/env bash
set -euo pipefail
ROOT=/home/claude/agent-arch-docs
YML="$ROOT/mkdocs.yml"

# カテゴリ表示名
declare -A CATNAME=(
[a-execution]="A：実行・セッション" [b-composition]="B：構成・分担" [c-io-contract]="C：入出力・契約化"
[d-tools-mcp]="D：ツール・MCP" [e-memory]="E：メモリ" [f-reliability]="F：信頼性・検証"
[g-security]="G：セキュリティ" [h-cost-performance]="H：コスト・性能" [i-observability]="I：観測性・LLMOps"
[j-abstraction]="J：抽象化" [k-human]="K：人間協調" [l-adoption]="L：導入・移行・統治"
)
ORDER=(a-execution b-composition c-io-contract d-tools-mcp e-memory f-reliability g-security h-cost-performance i-observability j-abstraction k-human l-adoption)

get_title() { grep -m1 '^title:' "$1" | sed -E 's/^title: *"?//; s/"?$//'; }

cat > "$YML" << 'HEAD'
site_name: AIエージェント本番組み込み アーキテクチャ・リファレンス
site_description: AIエージェントを本番システムに安全・堅牢・スケーラブルに組み込むためのアーキテクチャパターン集
site_author: ""
# GitHub Pages 公開時に正しいパスになるよう、実リポジトリに合わせて書き換える
site_url: https://USERNAME.github.io/agent-arch-docs/
repo_url: https://github.com/USERNAME/agent-arch-docs
repo_name: USERNAME/agent-arch-docs
edit_uri: edit/main/docs/

theme:
  name: material
  language: ja
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/weather-night
        name: ダークモードへ
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
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
      link: https://github.com/USERNAME/agent-arch-docs

# nav は scripts/build_nav.sh で再生成できる（CLAUDE.md 参照）
nav:
  - ホーム: index.md
  - はじめに:
      - 到達目標とエージェント特性: overview/agenda.md
      - 項目設計とカテゴリ分類: overview/schema.md
  - パターンカタログ:
      - 概要: patterns/index.md
HEAD

# 各カテゴリのnavを生成
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
      - パターン間の依存関係: integration/dependencies.md
      - 成熟度別ロードマップ: integration/roadmap.md
      - 選定ガイド: integration/selection-guide.md
      - リファレンスアーキテクチャ: integration/reference-architecture.md
      - 設計原則と組み合わせ方: integration/principles.md
TAIL
echo "mkdocs.yml written ($(wc -l < "$YML") lines)"
