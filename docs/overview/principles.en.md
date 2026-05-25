---
title: "Design Principles"
description: "Twelve design principles for enterprise AI agent architecture."
status: done
---

# Design Principles

The following twelve design principles underpin the enterprise AI agent architecture.

## Principle List

### 1. An Agent Never Exceeds the Requester's Permissions

Effective permission is the minimum of "capability ∩ requester's permission ∩ policy." Granting full access for convenience is prohibited.

A design where agents operate under an omnipotent service account exposes all users' data across all SaaS systems the moment of any breach. The baseline approach is a two-layer defense: obtain a token reduced to the requester's own permissions via OBO delegation, one per SaaS, and constrain actual data access through SaaS-side native authorization. In systems that do not support delegation, approximate permissions with a Permission Mirror — but always keep in mind that this is a cache, not an authoritative source.

Reference: [ID-4 Permission Mirror](../patterns/id-identity/id4-permission-mirror-least-of.md) / [ID-2 OBO](../patterns/id-identity/id2-identity-federation-obo.md)

### 2. Physically Separate the Workforce Surface from the Customer Surface

Structurally eliminate the most serious class of incident — customer-facing agents reaching internal data (and vice versa).

When workforce and customer-facing agents share the same IdP, data store, or network segment, a vulnerability in one surface can propagate to the other. Establishing physical separation of IdP and data stores, with zero network reachability between surfaces, from day one makes it possible to prove — in design reviews and penetration tests — that no cross-surface path exists.

Reference: [ID-1 Two-Surface Separation](../patterns/id-identity/id1-workforce-customer-split.md)

### 3. Companion Rather Than Replace

Do not replace the SoR; read from it and write via authorized procedures. Reuse existing integration assets.

Systems of Record like Salesforce, Workday, and ServiceNow hold the truth of enterprise business data. When agents bypass these systems and hold their own data, consistency breaks down and double management occurs. Agents call SoR APIs through authorized procedures, and writes are limited to validated domain services. If existing iPaaS flows (MuleSoft, Workato, etc.) are already in place, wrap them as MCP adapters and reuse them rather than building new connectors from scratch.

Reference: [RT-6 SoR Write Boundary](../patterns/rt-runtime/rt6-sor-write-boundary.md) / [IN-4 iPaaS Reuse](../patterns/in-integration/in4-existing-ipaas-reuse.md)

### 4. Question Data Before Copying It

Default to no-copy, JIT, and ACL-bundled. Aggregation is only for when the purpose is clear.

Copying and indexing all company-wide documents into a single vector DB severs the source ACL at the moment of copying, and delays in reflecting permission changes lead directly to leakage. The default is "do not copy" (JIT retrieval, federation). When copying is necessary, bundle ACL metadata and filter by requester permissions at search time. Data aggregation should also account for the mosaic effect (the risk that combining individually non-confidential data creates confidential information), and should be limited to a defined purpose and scope.

Reference: [KM-2 Context Mesh](../patterns/km-knowledge/km2-context-mesh.md) / [KM-1 Access-Controlled RAG](../patterns/km-knowledge/km1-access-controlled-rag.md)

### 5. Make the Org Graph the Single Source of Authority

Derive scope, sharing, approval, and delegation consistently from organizational structure.

"What is the range this agent can operate in?" "Who is the approver?" "How far does memory scope extend?" — to answer these questions consistently, a single organizational master consolidated from Workday, Okta, and project management tools is required. With the org graph as the authority, lifecycle events — transfers, promotions, resignations — are automatically reflected in the agent's permission scope, approval chain, and memory hierarchy.

Reference: [KM-3 Canonical Object & KG](../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) / [KM-4 Scoped Memory](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)

### 6. Guard with Identity and Policy, Not Prompts

Safety guarantees belong on the execution platform side. Prompts do not form security boundaries.

Writing "do not output confidential information" in a prompt is easily bypassed by prompt injection. Safety guarantees belong outside the LLM — in zero-trust authorization via PDP/PEP, policy code via OPA/Cedar, and masking via DLP. Managing policy as code enables change history, testing, and automated verification via CI/CD, ensuring policy consistency across the organization.

Reference: [ID-7 Policy-as-Code](../patterns/id-identity/id7-policy-as-code-guardrail.md) / [ID-6 Zero-Trust](../patterns/id-identity/id6-zero-trust-pdp-pep.md)

### 7. Attribute Every Action to Three Parties

Correlate human + agent + system with a correlation ID and audit across the enterprise.

If an agent's operation is only recorded as "executed by a service account," it is impossible to trace who requested it and what happened during an incident investigation. Every action must link three parties — "requester (human) · executor (agent/workload) · target system" — via correlation IDs. This three-party attribution audit trail is the foundation for compliance audits, incident response, and accountability tracking, and is extremely difficult to add retroactively.

Reference: [OB-2 Unified Audit](../patterns/ob-observability/ob2-unified-audit-lineage.md) / [OB-1 Observability Lake](../patterns/ob-observability/ob1-observability-lake.md)

### 8. Center Provides Guardrails and Paved Roads; Departments Own Business Logic

Two-layer governance balancing centralization and decentralization. The center owns infrastructure, authorization, audit, and evaluation; departments own domain knowledge and use cases.

The central platform team builds the Gateway, IdP integration, model Gateway, audit infrastructure, and evaluation pipeline. Departments build domain-specific agent templates, business logic, and use cases on top. When the center holds all business logic, departments lose agility; when departments independently build their own infrastructure, governance breaks down. The template factory pattern enables a division of labor where the center provides safe templates and departments fill in the parameters.

Reference: [GV-3 Department Factory](../patterns/gv-governance/gv3-department-agent-factory.md) / [GV-1 Control Plane](../patterns/gv-governance/gv1-agent-control-plane.md)

### 9. Natural Language Is a UI, Not an Internal Protocol

Always convert actions to structured commands. Never pass natural language directly to an API.

Passing LLM-generated natural language directly to downstream systems creates three problems: ambiguity of intent, injection risk, and non-reproducibility. Natural language input from users is received at the Gateway, and after the LLM interprets intent, it is converted to a structured command (Command Envelope) with actor, target_system, action, and params. Structured commands can be subjected to policy evaluation, audit recording, and idempotency guarantees — ensuring the determinism required for enterprise system integration.

Reference: [RT-5 Command Envelope](../patterns/rt-runtime/rt5-command-envelope.md) / [IN-2 SaaS Adapter](../patterns/in-integration/in2-saas-connector-adapter.md)

### 10. An Agent Is a "Managed Digital Business Actor That Processes a Work Queue"

Design as a registered, audited, permission-controlled, continuously evaluated execution actor — not a chatbot.

An agent is a first-class object within the enterprise, with attributes such as agent_id, owner_department, risk_tier, allowed_tools, and cost_budget. Agents not registered in the control plane are not permitted to execute; registered agents are continuously subject to evaluation, audit, and cost management. This design controls agent proliferation and enables enterprise-wide visibility into "who ran which agent, when, with what permissions."

Reference: [RT-9 Work Queue](../patterns/rt-runtime/rt9-work-queue-agent.md) / [GV-1 Control Plane](../patterns/gv-governance/gv1-agent-control-plane.md)

### 11. Rather Than Making AI Smarter, Make It Able to Work Safely Within Enterprise Boundaries

Intelligence is a given; the real challenge is permissions, integration, and governance.

Improving LLM capability is the model vendor's job. What enterprise architects must design is how to confine that intelligence within the enterprise's identity, permissions, auditing, and organizational structures. The unified entry point via Gateway, per-request verification via zero-trust authorization, and deterministic behavior control via policy code — only when these "cages" are in place can probabilistic intelligence be deployed in production at the scale of tens of thousands of users.

Reference: [EX-1 Gateway](../patterns/ex-experience/ex1-enterprise-agent-gateway.md) / [ID-6 Zero-Trust](../patterns/id-identity/id6-zero-trust-pdp-pep.md)

### 12. Design Not Whether, But to What Degree

Continuously tune autonomy, logs, budget, cache, and other continuous quantities using traces and evals.

Agent deployment is not a binary choice between "fully automated" and "manual." Autonomy tier boundaries, three-layer log separation (meta/body/aggregate), cost budget, cache TTL, and guardrail strength — all are continuous quantities, tuned incrementally based on business risk, data sensitivity, and organizational maturity. This tuning is not decided once at release and forgotten; it is updated continuously through feedback from Observability Lake traces and evaluation pipeline outputs.

Reference: [Degree Selection Criteria](../selection/degree/index.md) / [GV-7 Eval Pipeline](../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)

---

> Most concisely stated — **deploying AI agents in an enterprise is not about connecting an LLM to a business system; it is about safely introducing a new execution actor into the enterprise's identity, permissions, accountability, data, processes, auditing, and organizational structures.** Only when probabilistic intelligence is confined within the deterministic cage of permissions, organization, and audit does an enterprise AI agent capable of withstanding production at the scale of tens of thousands of users become possible.
