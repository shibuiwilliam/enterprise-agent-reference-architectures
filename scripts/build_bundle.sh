#!/bin/bash
# build_bundle.sh — Concatenate all pattern, selection, and integration pages
# into a single Markdown file for coding agent consumption.
# Output: docs/assets/full-reference.md (Japanese), docs/assets/full-reference.en.md (English)

set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p assets

# Strip YAML frontmatter from a markdown file
strip_frontmatter() {
  awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2{print}' "$1"
}

build_bundle() {
  local suffix="$1"  # "" for Japanese, ".en" for English
  local output="assets/full-reference${suffix}.md"

  echo "Building ${output}..."

  {
    if [ -z "$suffix" ]; then
      echo "# エンタープライズAIエージェント・アーキテクチャ・リファレンス（全文）"
      echo ""
      echo "> このファイルは全パターン・選定基準・統合ページを1つに結合したバンドルである。"
    else
      echo "# Enterprise AI Agent Architecture Reference (Full Bundle)"
      echo ""
      echo "> This file concatenates all pattern, selection, and integration pages into one bundle."
    fi
    echo ""
    echo "---"
    echo ""

    # Pattern pages
    for facet_dir in ex-experience gv-governance id-identity rt-runtime km-knowledge in-integration ob-observability; do
      for f in docs/patterns/${facet_dir}/*.md; do
        [ -f "$f" ] || continue
        [[ "$f" == *".en.md" ]] && continue
        [[ "$(basename "$f")" == "index.md" ]] && continue
        if [ -n "$suffix" ]; then
          local enf="${f%.md}.en.md"
          [ -f "$enf" ] && f="$enf"
        fi
        strip_frontmatter "$f"
        echo ""
        echo "---"
        echo ""
      done
    done

    # Selection criteria pages
    for sel_dir in degree tradeoff; do
      for f in docs/selection/${sel_dir}/*.md; do
        [ -f "$f" ] || continue
        [[ "$f" == *".en.md" ]] && continue
        [[ "$(basename "$f")" == "index.md" ]] && continue
        if [ -n "$suffix" ]; then
          local enf="${f%.md}.en.md"
          [ -f "$enf" ] && f="$enf"
        fi
        strip_frontmatter "$f"
        echo ""
        echo "---"
        echo ""
      done
    done

    # Integration pages
    for basename_f in dependency-chain cross-cutting-axes recipe; do
      local f="docs/integration/${basename_f}.md"
      if [ -n "$suffix" ]; then
        local enf="docs/integration/${basename_f}.en.md"
        [ -f "$enf" ] && f="$enf"
      fi
      [ -f "$f" ] || continue
      strip_frontmatter "$f"
      echo ""
      echo "---"
      echo ""
    done

    # Design principles
    local pf="docs/overview/principles.md"
    if [ -n "$suffix" ]; then
      local enf="docs/overview/principles.en.md"
      [ -f "$enf" ] && pf="$enf"
    fi
    [ -f "$pf" ] && strip_frontmatter "$pf"

  } > "${output}"

  local lines
  lines=$(wc -l < "${output}")
  echo "  → ${output}: ${lines} lines"
}

build_bundle ""
build_bundle ".en"
echo "Done."
