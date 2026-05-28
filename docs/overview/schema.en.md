---
title: "Item Design and Plane (Category) Classification"
description: "Defines the common description schema (8 items) and the 7-plane classification design for each pattern."
status: done
---

# Item Design and Plane (Category) Classification

## Common Description Schema

Each pattern is described uniformly across the following 8 items. The "Value Hypothesis" makes explicit where each pattern affects enterprise value, and "Pitfalls" is an independent item because it is directly connected to incidents.

| # | Item | Description |
|---|---|---|
| 1 | **Overview** | A one-sentence summary of what this pattern is |
| 2 | **Enterprise Problem It Solves** | What problem it solves, and which enterprise-specific pressures (leakage, silos, dynamic context, audit, cost) it addresses |
| 3 | **Value Hypothesis** | How this pattern affects which enterprise value KPIs (revenue/profit / business automation / project productivity / employee efficiency / decision-making speed), via which pathway. 1–3 lines, mapped to the measurement layers of [GV-10](../patterns/gv-governance/gv10-two-layer-value-measurement.md) |
| 4 | **Solution and Design** | The solution to the problem, plus the structure, data flow, state transitions, and implementation points that realize it |
| 5 | **Suitable / Unsuitable For** | Conditions under which this pattern works well, and conditions under which it causes harm or becomes excessive |
| 6 | **Component Technologies and Existing System Integration** | Representative technologies, standards, and target SaaS systems |
| 7 | **Pitfalls / Selection Guidance** | Typical failures and avoidance guidelines |
| 8 | **Related Patterns** | Links to other patterns that are similar, complementary, or contrasting |

!!! note "Diagrams in the Solution and Design Section"
    Structure, data flow, state transitions, and authorization sequences are described with mermaid. In particular, [ID-2 OBO Delegation](../patterns/id-identity/id2-identity-federation-obo.md), [ID-6 PDP/PEP](../patterns/id-identity/id6-zero-trust-pdp-pep.md), [RT-7 Saga](../patterns/rt-runtime/rt7-enterprise-saga.md), and [RT-10 Event-Driven](../patterns/rt-runtime/rt10-event-driven-orchestrator.md) are recommended to include sequence/flow diagrams.

## Plane (Category) Design

Patterns are classified into 7 planes according to "which design pressure they address." This aligns with responsibility boundaries and corresponds to the layer structure of the [Reference Architecture](../integration/architecture/index.md).

| Plane | Theme | Focus | Pattern Count |
|---|---|---|---|
| [Plane 1: Experience & Gateway (EX)](../patterns/ex-experience/index.md) | Entry point and delivery surface | Reach users where work happens; enforce control at the entry point | 3 |
| [Plane 2: Control & Governance (GV)](../patterns/gv-governance/index.md) | Governance and control | Central registry, model governance, evaluation, cost, incident response | 10 |
| [Plane 3: Identity & Trust (ID)](../patterns/id-identity/index.md) | Faithful propagation of permissions | Guarantee who's authority the agent operates under (highest design complexity of all planes) | 8 |
| [Plane 4: Runtime & Orchestration (RT)](../patterns/rt-runtime/index.md) | Division of labor, execution, automation | Responsibility allocation, autonomy, side effects, long-running tasks, events | 11 |
| [Plane 5: Knowledge, Memory & Context (KM)](../patterns/km-knowledge/index.md) | Capture and leverage knowledge | Supply cross-cutting context while preserving permissions | 7 |
| [Plane 6: Integration & Tools (IN)](../patterns/in-integration/index.md) | Existing system integration | Bundle rather than build; absorb system-specific differences | 4 |
| [Plane 7: Observability & Audit (OB)](../patterns/ob-observability/index.md) | Accountability | Make all actions reconstructable via three-party attribution | 2 |

### How to Read the Planes

Planes 1–2 handle "entry and governance"; Plane 3 handles "faithful propagation of permissions (high design complexity)"; Planes 4–6 handle "execution, knowledge, and integration"; Plane 7 handles "accountability." The dependency structure stacking these planes is shown in [Dependency Chains](../integration/dependency-chain.md).

### Enterprise-Specific Design Pressures

The design pressures referred to here are forces specific to enterprises, distinct from general software design.

| Design Pressure | Concrete Examples |
|---|---|
| **Leakage** | Customer data exfiltration, unauthorized cross-department access, PII sent to external LLMs |
| **Silos** | Data fragmentation across SaaS systems, vocabulary differences between departments, inability to integrate cross-cutting context |
| **Dynamic Context** | Permission changes from transfers or project endings, real-time reflection of organizational structure |
| **Audit** | Evidence trails for regulatory compliance, incident root-cause investigation, ensuring accountability |
| **Cost** | Department-level LLM token allocation, inference cost explosion in multi-agent setups, SaaS API rate consumption |

### Cross-Cutting Axes

In addition to the 7 planes, the following two function as cross-cutting axes spanning all planes.

- **Org Graph**: The foundation from which all planes consistently derive scope, delegation, and approval based on organizational structure. Serves as the basis for [ID-4](../patterns/id-identity/id4-permission-mirror-least-of.md), [RT-1](../patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md), [RT-4](../patterns/rt-runtime/rt4-human-approval-chain.md), and [KM-4](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md).
- **Zero Trust / Audit**: Every call is authorized and recorded with three-party attribution: human + agent + system. [ID-6](../patterns/id-identity/id6-zero-trust-pdp-pep.md) and [OB-2](../patterns/ob-observability/ob2-unified-audit-lineage.md) are the core.

## Extended Frontmatter (Machine-Readable Metadata)

In addition to the 8-section body schema, each pattern page includes the following mandatory YAML frontmatter fields. Coding agents can access this metadata in bulk via `docs/_machine/patterns.json`.

| Field | Type | Description |
|---|---|---|
| `id` / `pattern_id` | string | Pattern ID (e.g., `ID-2`) |
| `applies_when` | list | Condition tags where adoption is effective |
| `not_applicable_when` | list | Condition tags where adoption is inappropriate |
| `decision_keys` | list | DC/TO decision criteria IDs this pattern participates in |
| `value_drivers` | list | Enterprise value drivers (from unified vocabulary below) |
| `kpis` | list | Representative metrics linked to GV-10 |
| `prerequisites` / `requires` | list | Upstream pattern IDs this depends on |
| `related` / `required_by` | list | Bidirectional link target pattern IDs |
| `maturity_stage` | string | One of `foundation` / `execution` / `value_loop` |
| `mvp` | string | One-sentence minimum viable configuration |
| `cost_orientation` | string | Relative cost: `S` / `M` / `L` |

### Value Driver Vocabulary (Unified Tags)

| Tag | Meaning |
|---|---|
| `employee_efficiency` | Employee productivity improvement |
| `decision_quality` | Decision quality and speed improvement |
| `automation` | Business process automation |
| `revenue_growth` | Revenue and profit growth |
| `customer_value` | Customer experience and satisfaction improvement |
| `audit_compliance` | Audit and compliance assurance |
| `executive_decision` | Executive decision acceleration |
| `project_productivity` | Project productivity improvement |

### Decision Summary Block (Mandatory at End)

Each pattern page must include a machine-readable + human-readable Decision Summary YAML block at the end.

`scripts/build_machine_index.py` extracts these blocks to auto-generate `docs/_machine/patterns.json` and other machine-readable JSON files.
