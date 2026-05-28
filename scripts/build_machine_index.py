#!/usr/bin/env python3
"""Build machine-readable JSON indexes from the decision-driven architecture.

Generates:
  docs/_machine/decisions.json      — All decision pages with frontmatter + Decision Summary
  docs/_machine/building-blocks.json — Building blocks (old pattern IDs) extracted from decision pages
  docs/_machine/value-loop.json     — 6-node value loop with decision page references
  docs/_machine/departments.json    — Department pages with value usecases, KPIs, involved decisions
  docs/_machine/index.json          — Entry point listing all resources with URLs

Validates output against schemas/*.schema.json. Exits non-zero on failure.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    jsonschema = None
    print("WARNING: jsonschema not installed. Schema validation will be skipped.", file=sys.stderr)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MACHINE_DIR = DOCS / "_machine"
SCHEMAS_DIR = ROOT / "schemas"

# Domain directory names under docs/decisions/
DECISION_DOMAINS = [
    "ex-experience",
    "gv-governance",
    "id-identity",
    "rt-runtime",
    "km-knowledge",
    "in-integration",
    "ob-observability",
]

# Regex to match building block IDs like ID-2, RT-1, EX-1, etc.
BLOCK_ID_RE = re.compile(r"^(EX|GV|ID|RT|KM|IN|OB)-(\d+)", re.IGNORECASE)

# Regex to match decision IDs in frontmatter or filenames
DECISION_ID_RE = re.compile(r"([A-Z]{2})-D(\d+)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# YAML parsing helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    try:
        return yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return {}


def extract_decision_summary_yaml(path: Path) -> dict:
    """Extract the Decision Summary YAML block from the end of a file.

    Handles two formats:
      - ``decision_summary:`` (id-identity, in-integration, ob-observability)
      - ``decision:`` (ex-experience, gv-governance, km-knowledge, rt-runtime)
    Returns the inner dict in either case.
    """
    text = path.read_text(encoding="utf-8")

    # Find the YAML code block after "## Decision Summary"
    header_pos = text.find("## Decision Summary")
    if header_pos == -1:
        return {}

    remainder = text[header_pos:]
    pattern = r"```yaml\s*\n(.*?)```"
    match = re.search(pattern, remainder, re.DOTALL)
    if not match:
        return {}

    block = match.group(1)
    try:
        data = yaml.safe_load(block)
        if not isinstance(data, dict):
            return {}
        # Normalise: both formats → single dict
        if "decision_summary" in data:
            return data["decision_summary"]
        if "decision" in data:
            return data["decision"]
        return data
    except yaml.YAMLError:
        return {}


def extract_building_block_lines(path: Path) -> list[dict]:
    """Extract building block entries from the '必要な構成要素' section.

    Each line looks like:
      - **ID-2 Identity Federation & OBO**：description text... → 機械詳細は ...
    Returns list of {id, name, summary}.
    """
    text = path.read_text(encoding="utf-8")

    # Find the section
    header_pos = text.find("## 必要な構成要素")
    if header_pos == -1:
        return []

    # Find the next ## heading to bound the section
    next_heading = re.search(r"\n## ", text[header_pos + 1:])
    if next_heading:
        section = text[header_pos: header_pos + 1 + next_heading.start()]
    else:
        section = text[header_pos:]

    blocks = []
    # Pattern: - **XX-N Name**：summary...  (only building block prefixes)
    line_re = re.compile(
        r"^- \*\*((EX|GV|ID|RT|KM|IN|OB)-\d+)\s+(.+?)\*\*[：:](.+?)(?:→|$)",
        re.MULTILINE,
    )
    for m in line_re.finditer(section):
        block_id = m.group(1).strip()
        name = m.group(3).strip()
        summary = m.group(4).strip()
        # Truncate summary to first sentence or 200 chars for brevity
        if len(summary) > 300:
            # Find a good break point
            period_pos = summary.find("。", 100)
            if period_pos != -1 and period_pos < 300:
                summary = summary[: period_pos + 1]
            else:
                summary = summary[:300] + "…"
        blocks.append({"id": block_id, "name": name, "summary": summary})
    return blocks


def ensure_list(val) -> list:
    """Coerce a value to a list."""
    if val is None:
        return []
    if isinstance(val, str):
        return [val] if val else []
    if isinstance(val, list):
        return val
    return [val]


# ---------------------------------------------------------------------------
# Decision collection
# ---------------------------------------------------------------------------

def collect_decisions() -> list[dict]:
    """Collect decision data from all decision pages."""
    decisions = []

    for domain in DECISION_DOMAINS:
        dec_dir = DOCS / "decisions" / domain
        if not dec_dir.exists():
            continue
        for md in sorted(dec_dir.glob("*.md")):
            if md.name == "index.md" or md.name.endswith(".en.md"):
                continue

            fm = parse_frontmatter(md)
            ds = extract_decision_summary_yaml(md)

            # Determine decision ID
            did = fm.get("id", "")
            if not did:
                m = DECISION_ID_RE.search(fm.get("title", ""))
                if m:
                    did = f"{m.group(1).upper()}-D{m.group(2)}"
                else:
                    # Try filename
                    m = DECISION_ID_RE.search(md.stem)
                    if m:
                        did = f"{m.group(1).upper()}-D{m.group(2)}"
            if not did:
                continue

            entry = {
                "id": did,
                "domain": fm.get("domain", domain),
                "type": fm.get("type", ds.get("type", "")),
                "title": fm.get("title", ""),
                "description": fm.get("description", ""),
                "question": fm.get("question", ds.get("question", "")),
                "decides_among": ensure_list(fm.get("decides_among", [])),
                "building_blocks": ensure_list(fm.get("building_blocks", ds.get("building_blocks", []))),
                "related_decisions": ensure_list(fm.get("related_decisions", ds.get("related_decisions", []))),
                "value_drivers": ensure_list(fm.get("value_drivers", [])),
                "kpis": ensure_list(fm.get("kpis", [])),
                "maturity_stage": fm.get("maturity_stage", "foundation"),
                "mvp": fm.get("mvp", ds.get("mvp", "")),
                "cost_orientation": fm.get("cost_orientation", ds.get("cost", "M")),
                "status": fm.get("status", "draft"),
                "file": str(md.relative_to(DOCS)),
            }

            # Merge Decision Summary options if present
            if ds.get("options"):
                entry["options"] = ds["options"]
            if ds.get("default_recommendation"):
                entry["default_recommendation"] = ds["default_recommendation"]
            elif ds.get("default"):
                entry["default_recommendation"] = ds["default"]
            if ds.get("value_outcome"):
                vo = ds["value_outcome"]
                # Use DS value_outcome if frontmatter lacks them
                if not entry["value_drivers"] and vo.get("drivers"):
                    entry["value_drivers"] = ensure_list(vo["drivers"])
                if not entry["kpis"] and vo.get("kpis"):
                    entry["kpis"] = ensure_list(vo["kpis"])
            if ds.get("degree"):
                entry["degree"] = ds["degree"]

            decisions.append(entry)

    # Sort by domain prefix then number
    def sort_key(d):
        m = DECISION_ID_RE.match(d["id"])
        if m:
            domain_order = {"EX": 0, "ID": 1, "RT": 2, "KM": 3, "IN": 4, "GV": 5, "OB": 6}
            return (domain_order.get(m.group(1).upper(), 9), int(m.group(2)))
        return (9, 0)

    decisions.sort(key=sort_key)
    return decisions


# ---------------------------------------------------------------------------
# Building blocks collection
# ---------------------------------------------------------------------------

def collect_building_blocks(decisions: list[dict]) -> list[dict]:
    """Collect building block metadata from decision pages.

    Each building block (e.g. ID-2) is extracted from the '必要な構成要素' section
    of the decision page where it appears.
    """
    blocks_map: dict[str, dict] = {}  # keyed by block ID

    for domain in DECISION_DOMAINS:
        dec_dir = DOCS / "decisions" / domain
        if not dec_dir.exists():
            continue
        for md in sorted(dec_dir.glob("*.md")):
            if md.name == "index.md" or md.name.endswith(".en.md"):
                continue

            fm = parse_frontmatter(md)
            did = fm.get("id", "")
            if not did:
                m = DECISION_ID_RE.search(fm.get("title", ""))
                if m:
                    did = f"{m.group(1).upper()}-D{m.group(2)}"
                else:
                    m = DECISION_ID_RE.search(md.stem)
                    if m:
                        did = f"{m.group(1).upper()}-D{m.group(2)}"
            if not did:
                continue

            bb_lines = extract_building_block_lines(md)
            for bb in bb_lines:
                bid = bb["id"]
                if bid not in blocks_map:
                    blocks_map[bid] = {
                        "id": bid,
                        "name": bb["name"],
                        "decisions": [did],
                        "domain": domain,
                        "summary": bb["summary"],
                    }
                else:
                    # Append decision reference if not already present
                    if did not in blocks_map[bid]["decisions"]:
                        blocks_map[bid]["decisions"].append(did)

    # Sort by prefix and number
    blocks = list(blocks_map.values())

    def sort_key(b):
        m = BLOCK_ID_RE.match(b["id"])
        if m:
            prefix_order = {"EX": 0, "ID": 1, "RT": 2, "KM": 3, "IN": 4, "GV": 5, "OB": 6}
            return (prefix_order.get(m.group(1).upper(), 9), int(m.group(2)))
        return (9, 0)

    blocks.sort(key=sort_key)
    return blocks


# ---------------------------------------------------------------------------
# Department collection
# ---------------------------------------------------------------------------

def collect_departments() -> list[dict]:
    """Collect department data from department pages."""
    departments = []
    dept_dir = DOCS / "integration" / "departments"
    if not dept_dir.exists():
        return departments

    for md in sorted(dept_dir.glob("*.md")):
        if md.name == "index.md" or md.name.endswith(".en.md"):
            continue
        fm = parse_frontmatter(md)
        ds = extract_decision_summary_yaml(md)

        entry = {
            "id": fm.get("department", md.stem),
            "name": fm.get("title", md.stem),
            "value_drivers": ensure_list(fm.get("value_drivers", ds.get("value_drivers", []))),
            "value_usecases": ensure_list(ds.get("value_usecases", fm.get("value_usecases", []))),
            "kpis": ensure_list(fm.get("kpis", ds.get("kpis", []))),
            "applied_patterns": ensure_list(fm.get("applied_patterns", ds.get("applied_patterns", []))),
            "value_ladder": ensure_list(ds.get("value_ladder", fm.get("value_ladder", []))),
            "file": str(md.relative_to(DOCS)),
        }

        # Derive involved_decisions: find which decisions reference patterns used by this department
        # For now, extract from the page content if there are decision links
        text = md.read_text(encoding="utf-8")
        involved = []
        for m in re.finditer(r"\b([A-Z]{2})-D(\d+)\b", text):
            did = f"{m.group(1)}-D{m.group(2)}"
            if did not in involved:
                involved.append(did)
        # Also infer from decision links in markdown
        for m in re.finditer(r"decisions/[a-z-]+/([a-z]{2})-d(\d+)", text):
            did = f"{m.group(1).upper()}-D{m.group(2)}"
            if did not in involved:
                involved.append(did)
        entry["involved_decisions"] = involved

        departments.append(entry)

    return departments


# ---------------------------------------------------------------------------
# Value loop (static, references decision pages)
# ---------------------------------------------------------------------------

def generate_value_loop() -> dict:
    """Generate the 6-node value loop with decision page references."""
    return {
        "schema_version": "1.0.0",
        "description": "価値実現ループ — ユースケース選定から投資判断まで6ステップを繰り返す",
        "nodes": [
            {
                "id": "usecase_selection",
                "label": "価値ユースケース選定",
                "page": "integration/usecase-selection-guide.md",
                "description": "高価値・低リスクの初手を選ぶ",
                "related_decisions": ["EX-D1", "EX-D2"],
                "next": "recipe_quickwin",
            },
            {
                "id": "recipe_quickwin",
                "label": "最小安全ベースライン＋クイックウィン",
                "page": "integration/recipe.md",
                "description": "MVP構成で30-60日以内に初期価値を実証",
                "related_decisions": ["ID-D1", "ID-D2", "GV-D1", "RT-D1"],
                "next": "adoption",
            },
            {
                "id": "adoption",
                "label": "定着・アダプション",
                "page": "integration/adoption.md",
                "description": "チェンジマネジメントで利用率を引き上げ",
                "related_decisions": ["EX-D2", "GV-D7"],
                "next": "measurement",
            },
            {
                "id": "measurement",
                "label": "三層価値計測",
                "page": "decisions/gv-governance/gv-d7-value-measurement.md",
                "description": "採用定着→生産性→経営KPIの3層でROI追跡",
                "related_decisions": ["GV-D7", "GV-D4"],
                "next": "maturity_roadmap",
            },
            {
                "id": "maturity_roadmap",
                "label": "価値成熟度ロードマップ",
                "page": "integration/value-maturity-roadmap.md",
                "description": "段階的に適用範囲と自律度を拡大",
                "related_decisions": ["RT-D2", "GV-D3"],
                "next": "portfolio",
            },
            {
                "id": "portfolio",
                "label": "AI投資ポートフォリオ管理",
                "page": "integration/portfolio.md",
                "description": "計測結果に基づき再投資・改善・撤退を判断",
                "related_decisions": ["GV-D4", "GV-D7"],
                "next": "usecase_selection",
            },
        ],
    }


# ---------------------------------------------------------------------------
# Index generation
# ---------------------------------------------------------------------------

def generate_index(
    n_decisions: int,
    n_blocks: int,
    n_departments: int,
) -> dict:
    """Generate the master index listing all resources."""
    return {
        "schema_version": "1.0.0",
        "generated": str(date.today()),
        "resources": {
            "decisions": {
                "path": "decisions.json",
                "description": f"{n_decisions} decision pages with frontmatter and Decision Summary metadata",
                "count": n_decisions,
            },
            "building_blocks": {
                "path": "building-blocks.json",
                "description": f"{n_blocks} building blocks (architecture patterns) extracted from decision pages",
                "count": n_blocks,
            },
            "value_loop": {
                "path": "value-loop.json",
                "description": "6-node value realisation loop with decision references",
            },
            "departments": {
                "path": "departments.json",
                "description": f"{n_departments} department use-case bundles with KPIs and involved decisions",
                "count": n_departments,
            },
        },
        "value_drivers_vocabulary": [
            "employee_efficiency",
            "decision_quality",
            "automation",
            "revenue_growth",
            "customer_value",
            "audit_compliance",
            "executive_decision",
            "project_productivity",
        ],
    }


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def validate_json(data: object, schema_path: Path) -> list[str]:
    """Validate JSON data against a JSON Schema. Returns list of error messages."""
    if jsonschema is None:
        return []  # skip if not installed
    if not schema_path.exists():
        return []
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [str(e.message) for e in validator.iter_errors(data)]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    MACHINE_DIR.mkdir(parents=True, exist_ok=True)

    errors: list[str] = []

    # 1. Decisions
    decisions = collect_decisions()
    decisions_path = MACHINE_DIR / "decisions.json"
    decisions_path.write_text(
        json.dumps(decisions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generated {decisions_path.relative_to(ROOT)} ({len(decisions)} decisions)")

    schema = SCHEMAS_DIR / "decisions.schema.json"
    errs = validate_json(decisions, schema)
    if errs:
        errors.extend(f"decisions.json: {e}" for e in errs)

    # 2. Building blocks
    blocks = collect_building_blocks(decisions)
    blocks_path = MACHINE_DIR / "building-blocks.json"
    blocks_path.write_text(
        json.dumps(blocks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generated {blocks_path.relative_to(ROOT)} ({len(blocks)} building blocks)")

    schema = SCHEMAS_DIR / "building-blocks.schema.json"
    errs = validate_json(blocks, schema)
    if errs:
        errors.extend(f"building-blocks.json: {e}" for e in errs)

    # 3. Value loop
    value_loop = generate_value_loop()
    vl_path = MACHINE_DIR / "value-loop.json"
    vl_path.write_text(
        json.dumps(value_loop, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generated {vl_path.relative_to(ROOT)}")

    # 4. Departments
    departments = collect_departments()
    departments_path = MACHINE_DIR / "departments.json"
    departments_path.write_text(
        json.dumps(departments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generated {departments_path.relative_to(ROOT)} ({len(departments)} departments)")

    schema = SCHEMAS_DIR / "departments.schema.json"
    errs = validate_json(departments, schema)
    if errs:
        errors.extend(f"departments.json: {e}" for e in errs)

    # 5. Index
    index = generate_index(
        n_decisions=len(decisions),
        n_blocks=len(blocks),
        n_departments=len(departments),
    )
    index_path = MACHINE_DIR / "index.json"
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generated {index_path.relative_to(ROOT)}")

    schema = SCHEMAS_DIR / "index.schema.json"
    errs = validate_json(index, schema)
    if errs:
        errors.extend(f"index.json: {e}" for e in errs)

    # Summary
    if errors:
        print(f"\n{'='*60}")
        print(f"VALIDATION FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("All machine-readable indexes generated and validated successfully.")
    print(f"  decisions:       {len(decisions)}")
    print(f"  building-blocks: {len(blocks)}")
    print(f"  departments:     {len(departments)}")
    print(f"  value-loop:      6 nodes")
    sys.exit(0)


if __name__ == "__main__":
    main()
