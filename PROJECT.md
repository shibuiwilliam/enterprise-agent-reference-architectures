# PROJECT.md — Project Specification & Plan

This document defines the project's **specification and plan (what to build, why, and in what order)**. For day-to-day procedures, commands, and writing conventions, see `CLAUDE.md`.

---

## 1. Overview

- **Project name**: Enterprise AI Agent Architecture Reference
- **Deliverable**: A technical documentation site generated with MkDocs (Material theme) and published on GitHub Pages.
- **Purpose**: Provide reusable architecture patterns for safely integrating AI agents into enterprises—assuming tens of thousands of employees, diverse existing SaaS, strict permission management, and hierarchical organizations—in a form that enables side-by-side comparison and selection.
- **Core thesis**: The central challenge is not making AI smarter, but safely onboarding a new execution entity into the enterprise's existing ID, permissions, responsibilities, business processes, auditing, data boundaries, and organizational structure.
- **Target audience**: Enterprise architects, platform/infrastructure engineers, security/IAM teams, AI CoE, tech leads, SRE.

## 2. Primary Source (Source of Truth)

- The source for all content is **`reference/source-unified-enterprise.md`** (a consolidated reference from 3 reports: 7 facets, 45 patterns).
- Each page restructures the relevant section into a web-document-friendly format. Do not fabricate or pad content.
- Standards and proper nouns (NIST AI RMF / OWASP LLM Top 10 / OIDC / SCIM / RFC 8693 / NIST SP 800-207 / OPA / Cedar / MCP / CloudEvents / OpenTelemetry, and SaaS such as Salesforce / Workday / Okta) follow the scope of the source. When adding information beyond the source, cite explicitly and avoid definitive assertions.

## 3. Information Architecture & Directory Structure

Only `docs/` is published. `reference/` is writing material and is not published.

```text
.
├── PROJECT.md                  # This document (specification & plan)
├── CLAUDE.md                   # Operational manual for Claude Code
├── README.md                   # Quick start for humans
├── mkdocs.yml                  # Site configuration & navigation
├── pyproject.toml              # Dependencies managed by uv (mkdocs-material, pymdown-extensions)
├── uv.lock                     # uv lock file
├── .github/workflows/deploy.yml# GitHub Pages auto-deploy
├── scripts/build_nav.sh        # Regenerate nav from docs tree
├── reference/
│   └── source-unified-enterprise.md   # Primary source (unpublished)
└── docs/
    ├── index.md                # Home
    ├── overview/
    │   ├── agenda.md           # Step 1: Core thesis, taxonomy, org graph, 7 facets
    │   ├── schema.md           # Step 2: Schema design & facet classification
    │   └── principles.md       # Design principles
    ├── patterns/
    │   ├── index.md            # 7-facet overview
    │   ├── ex-experience/      # Facet 1 (index.md + EX-1..EX-4)
    │   ├── gv-governance/      # Facet 2 (GV-1..GV-10)
    │   ├── id-identity/        # Facet 3 (ID-1..ID-8) ★ Hardest
    │   ├── rt-runtime/         # Facet 4 (RT-1..RT-11)
    │   ├── km-knowledge/       # Facet 5 (KM-1..KM-7)
    │   ├── in-integration/     # Facet 6 (IN-1..IN-4)
    │   └── ob-observability/   # Facet 7 (OB-1..OB-2)
    ├── selection/
    │   ├── degree/             # Step 4: Degree criteria (index.md + DC-1..DC-9)
    │   └── tradeoff/           # Step 5: Tradeoff criteria (index.md + TO-1..TO-12)
    ├── integration/
    │   ├── dependency-chain.md # Step 6.1/6.2: Dependencies & composition recipes
    │   ├── cross-cutting-axes.md # Cross-cutting axes
    │   ├── recipe.md           # Composition recipes
    │   ├── value-maturity-roadmap.md # Value maturity roadmap
    │   ├── usecase-selection-guide.md # Use-case selection guide
    │   ├── adoption.md         # Adoption & change management
    │   ├── portfolio.md        # AI investment portfolio
    │   ├── departments/        # Department examples (index + 5 departments)
    │   └── architecture/       # Reference architecture (index + 4 axes)
    └── assets/                 # Images etc. (as needed)
```

## 4. Page Specifications

### 4.1 Pattern Page Common Schema (Required, Fixed Order)

Each pattern page has the following headings in this order. No section may be left empty.

1. `## Overview` — One-sentence summary of what the pattern is.
2. `## Enterprise Problem` — What problem it solves and which enterprise-specific forces (leakage / silos / dynamic context / audit / cost) it addresses.
3. `## Value Hypothesis` — Which enterprise value KPIs (revenue & profit / process automation / project productivity / employee efficiency / executive decision speed) this pattern impacts, and through what causal path. 1–3 lines.
4. `## Solution & Design` — The solution approach and its technical design: structure, data flow, state transitions, key implementation points. Diagrams in mermaid.
5. `## When to Use / When Not to Use` — Conditions where adoption is effective vs. harmful or excessive, presented as pairs.
6. `## Technology & System Integration` — Representative technologies, standards, and target SaaS.
7. `## Pitfalls & Selection Tips` — Typical anti-patterns and guidance for avoidance.
8. `## Related Patterns` — Relative links to similar, complementary, or contrasting patterns.

Frontmatter: `title` (`"<ID> <Name>"`), `description` (one sentence), `status` (`draft` → `done`).

### 4.2 Pattern List (All 45)

| ID | Name | File |
|---|---|---|
| EX-1 | Enterprise Agent Gateway | patterns/ex-experience/ex1-enterprise-agent-gateway.md |
| EX-2 | Embedded + Standalone Workbench | patterns/ex-experience/ex2-embedded-vs-portal.md |
| EX-3 | Channel-Agnostic Front Door | patterns/ex-experience/ex3-channel-agnostic-frontdoor.md |
| EX-4 | Trust & Value UX | patterns/ex-experience/ex4-trust-value-ux.md |
| GV-1 | Enterprise Agent Control Plane | patterns/gv-governance/gv1-agent-control-plane.md |
| GV-2 | Agent Catalog & Marketplace | patterns/gv-governance/gv2-agent-catalog-marketplace.md |
| GV-3 | Department Agent Factory | patterns/gv-governance/gv3-department-agent-factory.md |
| GV-4 | Industry Policy Pack | patterns/gv-governance/gv4-industry-policy-pack.md |
| GV-5 | Central Model Gateway | patterns/gv-governance/gv5-central-model-gateway.md |
| GV-6 | Version Registry | patterns/gv-governance/gv6-version-registry.md |
| GV-7 | Evaluation & Governance Pipeline | patterns/gv-governance/gv7-evaluation-governance-pipeline.md |
| GV-8 | Cost Quota & Chargeback | patterns/gv-governance/gv8-cost-quota-chargeback.md |
| GV-9 | Incident Response & Kill Switch | patterns/gv-governance/gv9-incident-response-kill-switch.md |
| GV-10 | Three-Layer Value Measurement | patterns/gv-governance/gv10-two-layer-value-measurement.md |
| ID-1 | Workforce/Customer Identity Split | patterns/id-identity/id1-workforce-customer-split.md |
| ID-2 | Identity Federation & OBO | patterns/id-identity/id2-identity-federation-obo.md |
| ID-3 | Workload / Agent Identity | patterns/id-identity/id3-workload-agent-identity.md |
| ID-4 | Permission Mirror & Least-of | patterns/id-identity/id4-permission-mirror-least-of.md |
| ID-5 | JIT Scoped Credentials | patterns/id-identity/id5-jit-scoped-credentials.md |
| ID-6 | Zero-Trust Runtime + PDP/PEP | patterns/id-identity/id6-zero-trust-pdp-pep.md |
| ID-7 | Policy-as-Code Guardrail | patterns/id-identity/id7-policy-as-code-guardrail.md |
| ID-8 | Consent & Access Transparency | patterns/id-identity/id8-consent-access-transparency.md |
| RT-1 | Org-Hierarchical Hub & Spoke | patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md |
| RT-2 | RACI-based Multi-Agent | patterns/rt-runtime/rt2-raci-multi-agent.md |
| RT-3 | Risk-Tiered Autonomy | patterns/rt-runtime/rt3-risk-tiered-autonomy.md |
| RT-4 | Human Approval Chain | patterns/rt-runtime/rt4-human-approval-chain.md |
| RT-5 | Command Envelope | patterns/rt-runtime/rt5-command-envelope.md |
| RT-6 | SoR Write Boundary | patterns/rt-runtime/rt6-sor-write-boundary.md |
| RT-7 | Enterprise Saga Agent | patterns/rt-runtime/rt7-enterprise-saga.md |
| RT-8 | Durable Workflow | patterns/rt-runtime/rt8-durable-workflow.md |
| RT-9 | Work Queue Agent | patterns/rt-runtime/rt9-work-queue-agent.md |
| RT-10 | Event-Driven Orchestrator | patterns/rt-runtime/rt10-event-driven-orchestrator.md |
| RT-11 | Project Digital Twin | patterns/rt-runtime/rt11-project-digital-twin.md |
| KM-1 | Access-Controlled RAG | patterns/km-knowledge/km1-access-controlled-rag.md |
| KM-2 | Context Mesh | patterns/km-knowledge/km2-context-mesh.md |
| KM-3 | Canonical Object & Knowledge Graph | patterns/km-knowledge/km3-canonical-object-knowledge-graph.md |
| KM-4 | Scoped Memory Hierarchy | patterns/km-knowledge/km4-scoped-memory-hierarchy.md |
| KM-5 | Purpose-Bound Context | patterns/km-knowledge/km5-purpose-bound-context.md |
| KM-6 | DLP & Redaction Boundary | patterns/km-knowledge/km6-dlp-redaction-boundary.md |
| KM-7 | Ephemeral Secure Context Bus | patterns/km-knowledge/km7-ephemeral-secure-context-bus.md |
| IN-1 | Enterprise Tool / MCP Gateway | patterns/in-integration/in1-tool-mcp-gateway.md |
| IN-2 | SaaS Connector Adapter | patterns/in-integration/in2-saas-connector-adapter.md |
| IN-3 | Rate / Quota Broker | patterns/in-integration/in3-rate-quota-broker.md |
| IN-4 | Existing iPaaS Reuse | patterns/in-integration/in4-existing-ipaas-reuse.md |
| OB-1 | Observability Lake | patterns/ob-observability/ob1-observability-lake.md |
| OB-2 | Unified Audit & Lineage | patterns/ob-observability/ob2-unified-audit-lineage.md |

### 4.3 Selection Criteria Page Schemas

#### Degree Criteria (DC-*) Page Schema (Required, Fixed Order)

1. `## Overview` — One-sentence summary of what this continuous parameter controls.
2. `## Harm from Too Little / Too Much` — Concrete harms from both extremes. Table format.
3. `## Decision Criteria` — Which input variables (impact, classification, job responsibility, etc.) determine the setting.
4. `## Tuning Mechanisms` — How to measure and adjust in production (integration with OB-1 / GV-7).
5. `## Related Patterns` — Relative links to corresponding patterns.

Frontmatter: `title` (`"DC-<N> <Name>"`), `description` (one sentence), `status` (`draft` → `done`).

#### Tradeoff Criteria (TO-*) Page Schema (Required, Fixed Order)

1. `## Overview` — What is in tension and why it appears to be a binary choice.
2. `## Comparison` — Aspect-by-aspect comparison table.
3. `## Decision Criteria` — Under which conditions to choose which side (the axis for drawing the line).
4. `## Hybrid & Staged Approaches` — Practical combined or staged strategies (where applicable).
5. `## Related Patterns` — Relative links to corresponding patterns.

Frontmatter: `title` (`"TO-<N> <Name>"`), `description` (one sentence), `status` (`draft` → `done`).

### 4.4 Selection Criteria Page List

#### Degree Criteria (DC-1 to DC-9)

| ID | Name | File |
|---|---|---|
| DC-1 | Autonomy Tier Boundaries (Risk-Tier Calibration) | selection/degree/dc1-risk-tier-boundary.md |
| DC-2 | Timeout, Retry & Budget (Cost Caps) | selection/degree/dc2-timeout-retry-budget.md |
| DC-3 | Prompt/Trace Log Granularity (Three-Layer Split) | selection/degree/dc3-log-granularity.md |
| DC-4 | Context Volume (top-k & Token Budget) | selection/degree/dc4-context-volume.md |
| DC-5 | Memory Retention & Forgetting (TTL & Scope) | selection/degree/dc5-memory-retention.md |
| DC-6 | Guardrail Strength (False Positives vs. Misses) | selection/degree/dc6-guardrail-strength.md |
| DC-7 | Cache Aggressiveness & JIT Credential TTL | selection/degree/dc7-cache-jit-ttl.md |
| DC-8 | Model Strength & Data-Classification Routing | selection/degree/dc8-model-routing.md |
| DC-9 | Canary Stages & Event-Driven Rate Limits | selection/degree/dc9-canary-event-throttle.md |

#### Tradeoff Criteria (TO-1 to TO-12)

| ID | Name | File |
|---|---|---|
| TO-1 | OBO Delegation vs. Service Account | selection/tradeoff/to1-obo-vs-service-account.md |
| TO-2 | Central Data Lake vs. Federated Context Mesh | selection/tradeoff/to2-lake-vs-mesh.md |
| TO-3 | Single Agent vs. RACI Multi-Agent | selection/tradeoff/to3-single-vs-multi-agent.md |
| TO-4 | Read-only vs. Write-capable (Staged Expansion) | selection/tradeoff/to4-readonly-vs-write.md |
| TO-5 | Copilot vs. Autopilot | selection/tradeoff/to5-copilot-vs-autopilot.md |
| TO-6 | Personal Memory vs. Project/Team Memory | selection/tradeoff/to6-personal-vs-team-memory.md |
| TO-7 | Full Prompt Logs vs. Selective Trace Logs | selection/tradeoff/to7-full-vs-selective-log.md |
| TO-8 | Central Platform vs. Department Federation | selection/tradeoff/to8-central-vs-federation.md |
| TO-9 | Custom Connectors vs. Existing iPaaS Reuse | selection/tradeoff/to9-custom-vs-ipaas.md |
| TO-10 | Internal/On-prem Model vs. External API | selection/tradeoff/to10-onprem-vs-external.md |
| TO-11 | Synchronous vs. Asynchronous | selection/tradeoff/to11-sync-vs-async.md |
| TO-12 | Guard with Prompts vs. Policy/Platform | selection/tradeoff/to12-prompt-vs-platform.md |

### 4.5 Non-Pattern, Non-Selection-Criteria Pages

| Page | Corresponding Step | Source Section |
|---|---|---|
| overview/agenda.md | Step 1 | Step 1 (thesis, taxonomy, org graph, 7 facets, standard alignment) |
| overview/schema.md | Step 2 | Step 2 |
| overview/principles.md | Design Principles | Step 6.6 |
| integration/dependency-chain.md | Step 6.1/6.2 | 6.1 Dependencies, 6.2 Composition recipes |
| integration/cross-cutting-axes.md | Cross-cutting axes | Org Graph & Zero Trust/Audit |
| integration/recipe.md | Composition recipes | 6.2 Composition recipes |
| integration/departments/*.md | Step 6.3 | 6.3 Department examples |
| integration/architecture/*.md | Step 6.5 | 6.5 Reference architecture |
| integration/value-maturity-roadmap.md | Value maturity roadmap | Step 6.4 |
| integration/usecase-selection-guide.md | Use-case selection guide | New (based on review) |
| integration/adoption.md | Adoption & change management | New (based on review) |
| integration/portfolio.md | AI investment portfolio | New (based on review) |

## 5. Writing Plan (Phases & Priorities)

Follow the maturity roadmap order, starting with the facets that deliver value in production first. **Facet 3 (Identity) is the hardest and most critical; solidify its skeleton early.**

- **Phase 0: Scaffold check** — Verify all stubs render in `mkdocs serve` and `mkdocs build --strict` passes.
- **Phase 1: Security foundation** — 2 overview pages + ID-2, ID-4, ID-1, ID-6, ID-7 (establish faithful permission propagation first) + KM-7.
- **Phase 2: Governance skeleton** — GV-1, GV-5, OB-1, OB-2, GV-9, EX-1.
- **Phase 3: Knowledge & integration** — KM-1, KM-2, KM-3, KM-4, IN-1, IN-2 + selection (DC-1–DC-9, TO-1–TO-12).
- **Phase 4: Runtime & automation** — RT-1–RT-11, remaining GV/EX/KM/IN/ID.
- **Phase 5: Integration chapter finalization** — integration pages (cross-link all patterns).

## 6. Definition of Done

Each page meets `status: done` when all of the following are satisfied:

- All sections of the common schema are filled with content (no empty sections, no TODOs) — for pattern pages.
- Frontmatter `title` matches nav, `description` is a single sentence.
- Internal links are valid (`mkdocs build --strict` passes with zero warnings).
- Diagrams are provided where needed (especially ID-2 OBO, RT-7 Saga, RT-10 Event-Driven — sequence/flow diagrams recommended).
- The page does not deviate from the intent of the corresponding primary source section.

## 7. Non-Goals

- Adding new patterns not in the source (propose via Issues separately).
- Providing complete implementation code (limit to technology names and minimal pseudo-code / config examples).
- Promoting or ranking specific vendor products.
- Casually presenting design examples that cross the workforce/customer boundary (violates the ID-1 principle).
