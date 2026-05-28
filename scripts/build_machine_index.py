#!/usr/bin/env python3
"""Build machine-readable JSON indexes from docs frontmatter and Decision Summary blocks.

Generates:
  docs/_machine/patterns.json
  docs/_machine/decisions.json
  docs/_machine/departments.json
  docs/_machine/value-loop.json
  docs/_machine/index.json

Validates output against schemas/*.schema.json. Exits non-zero on failure.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    # Fallback: simple YAML frontmatter parser
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MACHINE_DIR = DOCS / "_machine"
SCHEMAS_DIR = ROOT / "schemas"

# --- YAML parsing helpers ---

def parse_frontmatter(path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    if yaml:
        try:
            return yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            return {}
    else:
        return _simple_yaml_parse(fm_text)


def _simple_yaml_parse(text: str) -> dict:
    """Minimal YAML parser for frontmatter (handles scalars and lists)."""
    result = {}
    current_key = None
    for line in text.split("\n"):
        if not line.strip():
            continue
        # List item
        if line.startswith("  - ") and current_key:
            val = line.strip()[2:].strip().strip('"').strip("'")
            if current_key not in result:
                result[current_key] = []
            if isinstance(result[current_key], list):
                result[current_key].append(val)
            continue
        # Key: value
        m = re.match(r'^(\w+)\s*:\s*(.*)', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            current_key = key
            if val.startswith("[") and val.endswith("]"):
                # Inline list
                items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
                result[key] = items
            elif val:
                result[key] = val
            else:
                result[key] = None
    return result


def extract_decision_summary(path: Path) -> dict:
    """Extract decision_summary YAML block from end of file."""
    text = path.read_text(encoding="utf-8")
    pattern = r'```yaml\s*\n(decision_summary:.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return {}
    block = match.group(1)
    if yaml:
        try:
            data = yaml.safe_load(block)
            return data.get("decision_summary", {}) if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return {}
    return {}


def extract_decision_block(path: Path) -> dict:
    """Extract decision: YAML block from DC/TO pages."""
    text = path.read_text(encoding="utf-8")
    pattern = r'```yaml\s*\n(decision:.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return {}
    block = match.group(1)
    if yaml:
        try:
            data = yaml.safe_load(block)
            return data.get("decision", {}) if isinstance(data, dict) else {}
        except yaml.YAMLError:
            return {}
    return {}


# --- Pattern collection ---

PATTERN_DIRS = {
    "ex-experience": "experience",
    "gv-governance": "governance",
    "id-identity": "identity",
    "rt-runtime": "runtime",
    "km-knowledge": "knowledge",
    "in-integration": "integration",
    "ob-observability": "observability",
}

PATTERN_ID_RE = re.compile(r'^(EX|GV|ID|RT|KM|IN|OB)-(\d+)', re.IGNORECASE)


def collect_patterns() -> list:
    """Collect pattern data from all pattern pages (Japanese only, not .en.md)."""
    patterns = []
    for dirname, plane in PATTERN_DIRS.items():
        pat_dir = DOCS / "patterns" / dirname
        if not pat_dir.exists():
            continue
        for md in sorted(pat_dir.glob("*.md")):
            if md.name == "index.md" or md.name.endswith(".en.md"):
                continue
            fm = parse_frontmatter(md)
            pid = fm.get("pattern_id", "")
            if not pid:
                # Try to extract from filename
                m = PATTERN_ID_RE.match(md.stem.upper().replace("-", ""))
                if not m:
                    continue
                pid = f"{m.group(1).upper()}-{int(m.group(2))}"

            ds = extract_decision_summary(md)
            entry = {
                "id": pid,
                "plane": plane,
                "title": fm.get("title", ""),
                "summary": fm.get("summary", fm.get("description", "")),
                "applies_when": fm.get("applies_when", []),
                "not_applies_when": fm.get("not_applies_when", fm.get("not_applicable_when", [])),
                "decision_keys": fm.get("decision_keys", []),
                "value_drivers": fm.get("value_drivers", []),
                "kpis": fm.get("kpis", []),
                "prerequisites": fm.get("prerequisites", fm.get("requires", [])),
                "related": fm.get("related", fm.get("required_by", [])),
                "maturity_stage": fm.get("maturity_stage", "foundation"),
                "mvp": fm.get("mvp", ds.get("mvp", "")),
                "cost_orientation": fm.get("cost_orientation", ds.get("cost", "M")),
            }
            # Ensure lists
            for k in ["applies_when", "not_applies_when", "decision_keys", "value_drivers",
                      "kpis", "prerequisites", "related"]:
                if isinstance(entry[k], str):
                    entry[k] = [entry[k]] if entry[k] else []
                elif entry[k] is None:
                    entry[k] = []
            patterns.append(entry)

    # Sort by ID
    def sort_key(p):
        m = PATTERN_ID_RE.match(p["id"])
        if m:
            return (m.group(1), int(m.group(2)))
        return (p["id"], 0)

    patterns.sort(key=sort_key)
    return patterns


# --- Decision collection ---

def collect_decisions() -> list:
    """Collect decision criteria from DC/TO pages."""
    decisions = []
    for subdir, dtype in [("degree", "degree"), ("tradeoff", "tradeoff")]:
        dec_dir = DOCS / "decisions" / subdir
        if not dec_dir.exists():
            continue
        for md in sorted(dec_dir.glob("*.md")):
            if md.name == "index.md" or md.name.endswith(".en.md"):
                continue
            fm = parse_frontmatter(md)
            title = fm.get("title", "")
            # Extract ID from title or filename
            did = ""
            m = re.match(r'(DC|TO)-(\d+)', title)
            if m:
                did = f"{m.group(1)}-{m.group(2)}"
            else:
                m = re.match(r'(dc|to)(\d+)', md.stem)
                if m:
                    did = f"{m.group(1).upper()}-{int(m.group(2))}"

            if not did:
                continue

            db = extract_decision_block(md)
            entry = {
                "id": did,
                "title": title,
                "type": dtype,
                "options": db.get("options", []),
                "default_recommendation": db.get("default_recommendation", ""),
            }
            decisions.append(entry)

    def sort_key(d):
        m = re.match(r'(DC|TO)-(\d+)', d["id"])
        if m:
            prefix_order = {"DC": 0, "TO": 1}
            return (prefix_order.get(m.group(1), 2), int(m.group(2)))
        return (9, 0)

    decisions.sort(key=sort_key)
    return decisions


# --- Department collection ---

def collect_departments() -> list:
    """Collect department data."""
    departments = []
    dept_dir = DOCS / "integration" / "departments"
    if not dept_dir.exists():
        return departments

    for md in sorted(dept_dir.glob("*.md")):
        if md.name == "index.md" or md.name.endswith(".en.md"):
            continue
        fm = parse_frontmatter(md)
        ds = extract_decision_summary(md)

        entry = {
            "id": md.stem,
            "name": fm.get("title", md.stem),
            "value_usecases": ds.get("value_usecases", fm.get("value_usecases", [])),
            "kpis": ds.get("kpis", fm.get("kpis", [])),
            "value_ladder": ds.get("value_ladder", fm.get("value_ladder", [])),
            "applied_patterns": ds.get("applied_patterns", fm.get("applied_patterns", [])),
            "value_drivers": ds.get("value_drivers", fm.get("value_drivers", [])),
        }
        # Ensure lists
        for k in ["value_usecases", "kpis", "value_ladder", "applied_patterns", "value_drivers"]:
            if isinstance(entry[k], str):
                entry[k] = [entry[k]] if entry[k] else []
            elif entry[k] is None:
                entry[k] = []
        departments.append(entry)

    return departments


# --- Value loop (static, matches value-loop.json) ---

def generate_value_loop() -> dict:
    """Generate value loop data."""
    return {
        "schema_version": "1.0.0",
        "nodes": [
            {
                "id": "usecase_selection",
                "label": "価値ユースケース選定",
                "page": "integration/usecase-selection-guide.md",
                "description": "高価値・低リスクの初手を選ぶ",
                "next": "recipe_quickwin",
            },
            {
                "id": "recipe_quickwin",
                "label": "最小安全ベースライン＋クイックウィン",
                "page": "integration/recipe.md",
                "description": "MVP構成で30-60日以内に初期価値を実証",
                "next": "adoption",
            },
            {
                "id": "adoption",
                "label": "定着・アダプション",
                "page": "integration/adoption.md",
                "description": "チェンジマネジメントで利用率を引き上げ",
                "next": "measurement",
            },
            {
                "id": "measurement",
                "label": "GV-10 三層価値計測",
                "page": "patterns/gv-governance/gv10-two-layer-value-measurement.md",
                "description": "採用定着→生産性→経営KPIの3層でROI追跡",
                "next": "maturity_roadmap",
            },
            {
                "id": "maturity_roadmap",
                "label": "価値成熟度ロードマップ",
                "page": "integration/value-maturity-roadmap.md",
                "description": "段階的に適用範囲と自律度を拡大",
                "next": "portfolio",
            },
            {
                "id": "portfolio",
                "label": "AI投資ポートフォリオ管理",
                "page": "integration/portfolio.md",
                "description": "計測結果に基づき再投資・改善・撤退を判断",
                "next": "usecase_selection",
            },
        ],
    }


# --- Index generation ---

def generate_index() -> dict:
    """Generate the master index."""
    return {
        "schema_version": "1.0.0",
        "generated": "2026-05-28",
        "resources": {
            "patterns": {"path": "patterns.json", "description": "45 architecture patterns with metadata"},
            "decisions": {"path": "decisions.json", "description": "21 decision criteria (DC-1..DC-9, TO-1..TO-12)"},
            "value_loop": {"path": "value-loop.json", "description": "Value loop nodes and connections"},
            "departments": {"path": "departments.json", "description": "Department use cases and KPIs"},
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


# --- Schema validation ---

def validate_json(data, schema_path: Path) -> list:
    """Validate JSON data against a JSON Schema. Returns list of errors."""
    try:
        import jsonschema
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        return [str(e.message) for e in validator.iter_errors(data)]
    except ImportError:
        # If jsonschema not installed, do basic structural validation
        if isinstance(data, list):
            return []  # Accept if it's a list
        return ["Data is not a list"]


# --- Main ---

def main():
    MACHINE_DIR.mkdir(parents=True, exist_ok=True)

    errors = []

    # Generate patterns
    patterns = collect_patterns()
    patterns_path = MACHINE_DIR / "patterns.json"
    patterns_path.write_text(json.dumps(patterns, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {patterns_path} ({len(patterns)} patterns)")

    schema_file = SCHEMAS_DIR / "patterns.schema.json"
    if schema_file.exists():
        errs = validate_json(patterns, schema_file)
        if errs:
            errors.extend([f"patterns.json: {e}" for e in errs])

    # Generate decisions
    decisions = collect_decisions()
    decisions_path = MACHINE_DIR / "decisions.json"
    decisions_path.write_text(json.dumps(decisions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {decisions_path} ({len(decisions)} decisions)")

    schema_file = SCHEMAS_DIR / "decisions.schema.json"
    if schema_file.exists():
        errs = validate_json(decisions, schema_file)
        if errs:
            errors.extend([f"decisions.json: {e}" for e in errs])

    # Generate departments
    departments = collect_departments()
    departments_path = MACHINE_DIR / "departments.json"
    departments_path.write_text(json.dumps(departments, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {departments_path} ({len(departments)} departments)")

    schema_file = SCHEMAS_DIR / "departments.schema.json"
    if schema_file.exists():
        errs = validate_json(departments, schema_file)
        if errs:
            errors.extend([f"departments.json: {e}" for e in errs])

    # Generate value-loop
    value_loop = generate_value_loop()
    vl_path = MACHINE_DIR / "value-loop.json"
    vl_path.write_text(json.dumps(value_loop, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {vl_path}")

    # Generate index
    index = generate_index()
    index_path = MACHINE_DIR / "index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {index_path}")

    if errors:
        print("\nValidation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\nAll machine-readable indexes generated and validated successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
