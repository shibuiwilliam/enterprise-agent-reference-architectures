#!/usr/bin/env python3
"""Verify all applies_when/not_applicable_when tags exist in vocabulary.yaml."""
import yaml, sys
vocab = yaml.safe_load(open("docs/vocabulary.yaml"))
valid_tags = {t["id"] for t in vocab["tags"]}
index = yaml.safe_load(open("docs/patterns-index.yaml"))
errors = []
for p in index["patterns"]:
    for tag in p.get("applies_when", []) + p.get("not_applicable_when", []):
        if tag not in valid_tags:
            errors.append(f'{p["id"]}: unknown tag "{tag}"')
if errors:
    for e in errors: print(e, file=sys.stderr)
    sys.exit(1)
print(f"OK: all tags in {len(index['patterns'])} patterns are valid ({len(valid_tags)} vocabulary tags)")
