---
title: "Coding Agent Guide"
description: "Guide for coding agents to leverage this reference for proposing enterprise AI agent architectures."
status: done
---

# Coding Agent Guide

This chapter guides coding agents (GitHub Copilot, Claude Code, Cursor, etc.) in reading this reference to design and propose enterprise AI agent architectures.

## How to Read This Site

Coding agents should reference this site in the following order:

1. Read **`agents.md`** at the repository root first to understand the reasoning process and output template.
2. Retrieve schema version and resource paths from **`docs/_machine/index.json`**.
3. Reference `patterns.json`, `decisions.json`, `value-loop.json`, and `departments.json` as needed.
4. Read individual markdown pages only when details are required.

## Reasoning Process: Requirements → Candidate Patterns → Architecture Proposal

### Step 1: Structuring Requirements

Extract the following from user requirements:

| Extraction Item | Example |
|---|---|
| Purpose (value_drivers) | revenue_growth, automation |
| Constraints (regulation, sensitivity) | Financial industry (GV-4 applies), high sensitivity |
| Current SaaS | Salesforce, Workday, Slack |
| Allowed autonomy | Copilot (TO-5) |
| Organization size | 5,000 employees, 3 business units |

### Step 2: Evaluating Decision Criteria

Identify relevant DC/TO from `decisions.json` and match each option's pick_when conditions against requirements.

### Step 3: Pattern Selection and Dependency Resolution

Retrieve patterns required by selected options from `patterns.json` and recursively resolve prerequisites.

### Step 4: Composition

- Minimum safe baseline (ID-1 + ID-6 + GV-1 + OB-2)
- 30-60 day quick wins (read-only use cases)
- Expansion phase (write permissions, multi-agent)
- Adoption & measurement (GV-10 + adoption)
- Investment decisions (portfolio)

### Step 5: Output Generation

Generate architecture proposals for humans following the output template defined in `agents.md`.

## Output Template

Proposals should follow this structure:

| Section | Content |
|---|---|
| Purpose & KPIs | Value drivers and target metrics |
| Adopted Patterns (by plane) | Patterns for each of the 7 facets |
| Decision Rationale | DC/TO selections and reasoning |
| Minimum Safe Baseline + Quick Wins | MVP composition and initial value |
| Value Ladder | Visibility → Analysis → Execution |
| Adoption, Measurement & Investment | Operational phase design |
| Risks & Open Items | Remaining trade-offs |

## Machine-Readable Data Reference

Parse JSON files under `docs/_machine/` directly.

| File | Purpose |
|---|---|
| `index.json` | Entry point, schema version check |
| `patterns.json` | Pattern search & dependency resolution |
| `decisions.json` | Decision criteria evaluation |
| `value-loop.json` | Value loop navigation |
| `departments.json` | Department use case reference |

## Value Driver Vocabulary (Unified Tags)

| Tag | Meaning |
|---|---|
| employee_efficiency | Employee productivity improvement |
| decision_quality | Decision quality and speed improvement |
| automation | Business process automation |
| revenue_growth | Revenue and profit growth |
| customer_value | Customer experience and satisfaction improvement |
| audit_compliance | Audit and compliance assurance |
| executive_decision | Executive decision acceleration |
| project_productivity | Project productivity improvement |

## Related Pages

- [Use-Case Selection Guide](../integration/usecase-selection-guide.md)
- [Composition Recipes](../integration/recipe.md)
- [Adoption & Change Management](../integration/adoption.md)
- [GV-10 Three-Layer Value Measurement](../decisions/gv-governance/gv-d7-value-measurement.md)
- [Decision Guide](../decisions/decision-guide.md)
