---
title: "Pattern Catalog"
description: "A catalog of 45 enterprise AI agent architecture patterns across 7 dimensions."
---

# Pattern Catalog

Patterns are classified into 7 dimensions based on "which design pressures (leakage, silos, dynamic context, auditing, cost) they address." This also aligns with responsibility boundaries and corresponds to the layer structure of the [Reference Architecture](../integration/architecture/index.md).

Each pattern is described in a common schema (**Overview / Design / Enterprise Problem Addressed / When to Use & Not to Use / Component Technologies & System Integration / Pitfalls & Selection Criteria / Related Patterns**). For the schema definition, see [Item Design](../overview/schema.md).

## Dimension (Category) Overview

| Dimension | Theme | Focus | Count |
|---|---|---|---|
| [Dimension 1: Experience & Gateway (EX)](ex-experience/index.md) | Entry points and delivery surfaces | Deliver where work happens, govern at the entry | 3 |
| [Dimension 2: Control & Governance (GV)](gv-governance/index.md) | Governance and control | Registry, model control, evaluation, cost, incident response | 10 |
| [Dimension 3: Identity & Trust (ID)](id-identity/index.md) | Faithful permission propagation | Guarantee who's executing with whose authority (highest design complexity) | 8 |
| [Dimension 4: Execution & Orchestration (RT)](rt-runtime/index.md) | Division of labor, execution, automation | Responsibility assignment, autonomy levels, side effects, long-running processes, events | 11 |
| [Dimension 5: Knowledge, Memory & Context (KM)](km-knowledge/index.md) | Use without leaking | Supply cross-context while maintaining permissions | 7 |
| [Dimension 6: Integration & Tools (IN)](in-integration/index.md) | Existing system integration | Bundle without building, absorb proprietary differences | 4 |
| [Dimension 7: Observability, Evaluation & Audit (OB)](ob-observability/index.md) | Accountability | Make all actions reconstructable with tripartite attribution | 2 |

!!! tip "How to Read"
    Dimensions 1–2 are "entry points and governance," Dimension 3 is "faithful permission propagation (highest design complexity)," Dimensions 4–6 are "execution, knowledge, and integration," and Dimension 7 is "accountability." For accumulated dependency relationships, see [Dependencies and Dependency Chains](../integration/dependency-chain.md).

!!! info "Minimum Safety Set: Start Here"
    There is no need to introduce all 45 patterns at once. The following 6 patterns form the "minimum safety set" — with just these, a reference-type agent can operate safely and be extended incrementally.

    1. **[GV-1 Agent Control Plane](gv-governance/gv1-agent-control-plane.md)** — Agent registration and lifecycle management
    2. **[ID-2 Identity Federation & OBO](id-identity/id2-identity-federation-obo.md)** — Operating SaaS with the requester's own permissions
    3. **[ID-4 Permission Mirror & Least-of](id-identity/id4-permission-mirror-least-of.md)** — Least privilege composition
    4. **[RT-6 SoR Write Boundary](rt-runtime/rt6-sor-write-boundary.md)** — Write operation boundary control
    5. **[KM-1 Access-Controlled RAG](km-knowledge/km1-access-controlled-rag.md)** — Permission-aware knowledge search
    6. **[OB-2 Unified Audit & Lineage](ob-observability/ob2-unified-audit-lineage.md)** — Tripartite attribution audit trail

    Start with this minimum set and expand in order as business requirements mature: governance (GV-5/GV-7) → advanced execution (RT-3/RT-4/RT-7) → knowledge enrichment (KM-2/KM-4). For details, see the [Maturity Roadmap](../integration/architecture/index.md).
