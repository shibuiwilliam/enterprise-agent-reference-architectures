#!/bin/bash
# check_sync.sh — Check if English .en.md files are older than their Japanese .md counterparts.
set -euo pipefail
cd "$(dirname "$0")/.."

out_of_sync=0
missing=0
total=0

while IFS= read -r ja_file; do
  total=$((total + 1))
  en_file="${ja_file%.md}.en.md"

  if [ ! -f "$en_file" ]; then
    echo "MISSING: $en_file"
    missing=$((missing + 1))
    out_of_sync=$((out_of_sync + 1))
    continue
  fi

  # macOS stat uses -f %m, Linux uses -c %Y
  ja_mtime=$(stat -f %m "$ja_file" 2>/dev/null || stat -c %Y "$ja_file" 2>/dev/null)
  en_mtime=$(stat -f %m "$en_file" 2>/dev/null || stat -c %Y "$en_file" 2>/dev/null)

  if [ "$ja_mtime" -gt "$en_mtime" ]; then
    echo "OUT OF SYNC: $(basename "$ja_file") (ja newer)"
    out_of_sync=$((out_of_sync + 1))
  fi
done < <(find docs -name "*.md" -not -name "*.en.md" -not -path "*/assets/*" | sort)

echo ""
echo "Checked: $total files"
if [ "$missing" -gt 0 ]; then
  echo "Missing English versions: $missing"
fi
if [ "$out_of_sync" -gt 0 ]; then
  echo "Out of sync: $out_of_sync"
  exit 1
fi
echo "All files in sync."
