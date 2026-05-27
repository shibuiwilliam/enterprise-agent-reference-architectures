---
title: "Coding Agent Digest"
description: "Single-file digest aggregating all 46 patterns, selection criteria, dependency graph, and interfaces for coding agents."
---

# Coding Agent Digest

> This file is designed to be loaded first by coding agents (Claude Code, Cursor, GitHub Copilot Workspace, etc.). After grasping the overall picture, proceed to individual pattern pages for details.

## How to Use

1. Use the table below to identify candidate patterns
2. Check the `requires` column for dependencies
3. Verify scenario fit using the `applies_when` column
4. Retrieve interface definitions from `## Interfaces` in individual pattern pages
5. For structured data, load `patterns-index.yaml` and `selection-rules.yaml`

## All Patterns

| ID | Name | Facet | Requires | Applies When (representative) | Key Interfaces |
|---|---|---|---|---|---|
| EX-1 | Enterprise Agent Gateway | experience | ID-1, ID-2, ID-6 | enterprise_scale, multi_channel, audit_required | Authentication & Risk Classification, Rate Control, Audit Entry Point |
| EX-2 | Embedded Workbench Channel Placement | experience | EX-1, EX-3 | multi_channel, enterprise_scale, long_running | Embedded UI, Standalone Workbench, Channel Adapter |
| EX-3 | Channel-Agnostic Frontdoor | experience | EX-1, ID-2 | multi_channel, audit_required, enterprise_scale | Channel Adapter, Unified Session Store, Unified Audit Logger |
| EX-4 | Trust & Value UX | experience | EX-1, KM-1, RT-3 | enterprise_scale, adoption_challenge, prod_deployment | Citation & Confidence Layer, Progressive Confirmation UI, Value Feedback Dashboard |
| GV-1 | Enterprise Agent Control Plane | governance | ID-7 | multi_department, enterprise_scale, audit_required | Agent Registry, Lifecycle Review Gate, Execution Enforcement |
| GV-2 | Agent Catalog & Marketplace | governance | GV-1 | multi_department, enterprise_scale, prod_deployment | Catalog UI/API, Access Request Workflow, Usage Analytics & Quality Score |
| GV-3 | Department Agent Factory | governance | GV-1, GV-2, ID-4, GV-4 | multi_department, enterprise_scale, frequent_perm_chg | Role-Based Template Store, Low-Code Builder, IdP Role Change Listener |
| GV-4 | Industry Policy Pack | governance | ID-6, ID-7 | regulated_industry, multi_department, enterprise_scale | Policy Pack Definition, Policy Engine Deployment, Evaluation Rubric |
| GV-5 | Central Model Gateway | governance | GV-1 | enterprise_scale, confidential_data, external_llm_api | Model Approval Check, Data Classification Router, Token & Cost Meter |
| GV-6 | Version Registry | governance | OB-1 | continuous_updates, prod_deployment, audit_required | Version Tag per Execution, PR-Gated Change Flow, Canary + Auto-Rollback |
| GV-7 | Evaluation & Governance Pipeline | governance | OB-1 | prod_deployment, continuous_updates, regulated_industry | Offline Evaluation Gate, Security Evaluation, Production Drift Monitor |
| GV-8 | Cost Quota & Chargeback | governance | GV-1, GV-5 | enterprise_scale, cost_mgmt_needed, multi_agent | cost_center Tag Attribution, Budget Alert & Degradation, ROI Dashboard |
| GV-9 | Incident Response & Kill Switch | governance | OB-1, OB-2, GV-1, GV-5 | prod_deployment, enterprise_scale | Granular Kill Switch, Trace Preservation, Incident Response Runbook |
| GV-10 | Three-Layer Value Measurement | governance | GV-8, OB-1 | enterprise_scale, roi_justification, multi_agent | Layer 0 Adoption Metrics, Layer 1 & 2 Business KPI Joiner, ROI Dashboard |
| ID-1 | Workforce/Customer Split | identity | — | customer_facing, confidential_data, enterprise_scale | Dual IdP Boundary, Explicit Cross-Boundary Gate, Tenant Isolation |
| ID-2 | Identity Federation & OBO | identity | — | cross_saas, audit_required, write_operations | Token Broker, SaaS Native Authorization, Audit Delegation Chain |
| ID-3 | Workload Agent Identity | identity | ID-5, ID-6 | autonomous_exec, audit_required, kubernetes_cloud | Workload Certificate Issuer, Dual Representation Audit Record, Least-Privilege Workload Scope |
| ID-4 | Permission Mirror & Least-of Faithful Access | identity | — | cross_saas_search, frequent_perm_chg, legacy_saas_mix | ACL Sync Pipeline, Effective Permission Calculator, Stale-Access Monitor |
| ID-5 | JIT Scoped Credentials | identity | ID-6 | cross_saas, high_risk_ops, vault_sts_infra | Credential Broker, PDP Pre-Issuance Check, Credential Audit Trail |
| ID-6 | Zero-Trust PDP/PEP | identity | — | confidential_data, cross_saas, regulated_industry | Central PDP, Distributed PEP, Org Graph Attribute Feed |
| ID-7 | Policy-as-Code Guardrail | identity | ID-6 | regulated_industry, enterprise_scale, multi_agent | Structured Policy Input, Policy Engine, Policy Version & Test Gate |
| ID-8 | Consent & Access Transparency | identity | ID-2, ID-4, ID-5 | personal_data, privacy_regulation, adoption_challenge | Consent Screen, Consent Registry, Revocation & Instant Token Invalidation |
| RT-1 | Org-Hierarchical Hub & Spoke | runtime | ID-4 | multi_department, enterprise_scale, multi_agent | Hub Agent, Domain Spoke Agent, Capability Registry |
| RT-2 | RACI-based Multi-Agent Orchestration | runtime | OB-2 | multi_department, high_risk_ops, hitl_approval | Orchestrator, Decision Log, Approval Gate |
| RT-3 | Risk-Tiered Autonomy | runtime | ID-7 | write_operations, high_risk_ops, enterprise_scale | Risk Scoring Engine, Policy Engine, Approval Workflow |
| RT-4 | Human Approval Chain | runtime | RT-8, ID-7 | high_risk_ops, hitl_approval, org_chart_maintained | Approver Resolution Engine, Workflow Tool Notification, Decision Log |
| RT-5 | Intent-to-Enterprise Command Envelope | runtime | — | cross_saas, write_operations, audit_required | Intent Parser + Entity Extractor, Policy Engine, SaaS Adapter |
| RT-6 | System-of-Record Write Boundary | runtime | RT-5 | sor_writes, sox_internal_ctrl, multi_agent | Domain Service, SoE Draft Store, Audit Trail |
| RT-7 | Enterprise Saga Agent | runtime | RT-8 | multi_saas_saga, cross_saas, write_operations | Saga Orchestrator, Idempotency Key Manager, Compensation Action Library |
| RT-8 | Durable Enterprise Agent Workflow | runtime | OB-1 | long_running, hitl_approval, audit_required | Workflow Definition, Activity Function, Budget / Step Limit Guard |
| RT-9 | Enterprise Work Queue Agent | runtime | — | itsm_queue, enterprise_scale, async_processing | Queue Consumer, Escalation Handler, SLA Monitor |
| RT-10 | Event-Driven Enterprise Orchestrator | runtime | RT-7, RT-8 | event_driven, async_processing, cross_saas | Event Gateway, Debounce / Rate Limiter, Durable Workflow Engine |
| RT-11 | Project Workspace / Digital Twin Agent | runtime | KM-1, KM-4, ID-4 | project_team, cross_saas_search, persistent_memory | Project Workspace Provisioner, GraphRAG Memory, Decision Log Store |
| KM-1 | Access-Controlled Enterprise RAG | knowledge | ID-2, ID-4 | cross_saas_search, frequent_perm_chg, confidential_data | Ingest Pipeline with ACL Embedding, Permission Filter, Hybrid Search + Reranker |
| KM-2 | Access-Controlled Context Mesh | knowledge | ID-2 | confidential_data, data_residency, cross_saas | Context Router, Context Provider, Context Package Builder |
| KM-3 | Canonical Enterprise Object Model & Knowledge Graph | knowledge | — | multi_department, cross_saas, enterprise_scale | Entity Resolution Engine, Knowledge Graph, Graph Traversal API |
| KM-4 | Scoped Memory Hierarchy | knowledge | — | persistent_memory, multi_department, personal_data | Memory Scope Partitioner, Lifecycle Event Handler, Memory Review UI |
| KM-5 | Purpose-Bound Context Package | knowledge | — | multi_purpose_agent, confidential_data, privacy_regulation | Purpose Policy Store, Context Builder, DLP / Classification Filter |
| KM-6 | DLP & Redaction Boundary | knowledge | — | personal_data, external_llm_api, privacy_regulation | Input DLP Gate, Output DLP Gate, Log Filter |
| KM-7 | Ephemeral Secure Context Bus | knowledge | — | top_secret_data, privacy_regulation, regulated_industry | DLP Proxy, Isolated Inference Environment, Sealed Audit Metadata Sink |
| IN-1 | Enterprise Tool / MCP Gateway | integration | ID-6 | multi_agent, cross_saas, audit_required | Tool Catalog, Auth / Authz Layer, Audit Recorder |
| IN-2 | SaaS Connector Adapter | integration | — | cross_saas, multi_agent, enterprise_scale | Canonical Tool Interface, SaaS-Specific Adapter, Error Normalizer |
| IN-3 | Rate / Quota Broker | integration | — | high_api_volume, enterprise_scale, async_processing | Token Bucket per SaaS, Priority Queue, Centralized Retry Handler |
| IN-4 | Existing iPaaS Reuse | integration | IN-1 | existing_ipaas, cross_saas, enterprise_scale | MCP Adapter, iPaaS Flow, Contract Test Suite |
| OB-1 | Enterprise Agent Observability Lake | observability | — | prod_deployment, enterprise_scale | OTel Instrumentation Layer, Three-Layer Storage, Replay Tool |
| OB-2 | Unified Audit & Lineage | observability | GV-1, RT-8 | prod_deployment, audit_required, regulated_industry | Three-Party Audit Record, Correlation ID Stitcher, SIEM Integration |

## Selection Quick Reference (Tradeoffs)

| Question | Answer | Reference |
|---|---|---|
| How should the agent authenticate to downstream SaaS? | Personal assistance=OBO (ID-2), Autonomous batch=Agent ID (ID-3), High-risk irreversible=Hybrid (OBO + HitL) | TO-1 |
| Centralized data lake or federated Context Mesh? | Public data=Central lake (KM-1 with ACL), Confidential SaaS=Federated Mesh (KM-2), Mixed=Hybrid | TO-2 |
| Single agent or RACI multi-agent architecture? | Default to single agent. Multi-agent only when multiple departments have independent approval requirements | TO-3 |
| What write permission level should be granted to the agent? | Start with read-only. Promote to auto-write after eval for reversible low-risk. Irreversible requires HitL | TO-4 |
| Copilot (human-assisted) or Autopilot (autonomous)? | Start all operations as Copilot. Expand to Autopilot incrementally only after eval, canary, and kill switch are in place | TO-5 |
| Personal scope memory or shared project/team memory? | Personal settings/confidential=Personal Enclave, Shared knowledge=Project Workspace, Mixed=physical separation required | TO-6 |
| Full prompt logs or selective trace logs? | Standard=Three-layer separation (metadata→Trace DB, body→encrypted storage, aggregates→DWH). Top-secret=metadata only | TO-7 |
| Centralized AI governance or federated to departments? | Auth/audit/model control=central. Domain knowledge/use cases=delegate to departments (two-layer governance) | TO-8 |
| Build integration connectors in-house or reuse existing iPaaS? | Reuse existing iPaaS after verifying authorization granularity and audit trail. New integrations=MCP-standardized (IN-1) | TO-9 |
| Internal/on-premise models or external inference APIs? | Top-secret/regulated=internal/on-prem required. General data=external API permitted (after DPA confirmation). Mixed=auto-route via GV-5 | TO-10 |
| Synchronous or asynchronous processing? | Simple Q&A under 5s=synchronous. Over 10s or approval steps or multiple API calls=async (RT-8). Multi-SaaS transactions=Saga (RT-7) | TO-11 |
| Safety controls via prompts or via execution platform? | Access control/approval/DLP/sandbox=execution platform required. Prompts=quality and behavior tuning only | TO-12 |

## Selection Quick Reference (Degree)

| Parameter | Starting Point | Adjustment Criteria | Reference |
|---|---|---|---|
| Autonomy tier boundary | All writes require approval, reads auto-execute | Irreversibility × impact scope × data classification × requester role. Financial/contractual/external=multi-approver | DC-1 |
| Timeout, retry, cost budget | Q&A: TTFT=5s, total=30s, retries=2. Document analysis: total=300s | Human approval steps: remove global timeout, use durable workflow. Non-idempotent ops: retries=0 | DC-2 |
| Log granularity and storage tier | Standard=three-layer separation. Regulated data needs per-classification retention policy | Top-secret=metadata only. Cost constraints=error + high-risk + random N% sampling | DC-3 |
| Context volume (top-k, token budget) | Q&A: top-k=3, budget=25%. Multi-source analysis: top-k=10, budget=50% + reranker | Confidential data must be DLP-masked before injection. Injecting all available data is an anti-pattern | DC-4 |
| Memory retention TTL | Session=discard at end. Personal (high-frequency)=90-day rolling TTL | Departure/transfer/project-end triggers immediate expiry. Individual right to erasure must be in the design | DC-5 |
| Guardrail strength | Low-risk routes=lightweight guardrails. High-risk routes=strict (minimize false negatives) | Measure FP and FN rates via GV-7; adjust threshold based on which harm (disruption vs. incident) is larger | DC-6 |
| Cache aggressiveness and JIT TTL | Stable, non-personalized, low-risk=aggressive cache (TTL in hours) | Personalized/confidential/side-effect ops=disable cache. Force expire on permission change events | DC-7 |
| Model routing | Simple task + non-sensitive=lightweight model. Low confidence=escalate to stronger model | Top-secret data=VPC/on-prem path only. Automate routing via GV-5, never rely on manual config | DC-8 |
| Canary rollout stages and event throttle | 1%→5%→25%→100% multi-stage rollout as baseline | Auto-rollback via GV-6 on quality/error/cost threshold breach. Event storms: debounce + rate limit + budget cap | DC-9 |

## Dependency Adjacency List

```yaml
EX-1: [ID-1, ID-2, ID-6]
EX-2: [EX-1, EX-3]
EX-3: [EX-1, ID-2]
EX-4: [EX-1, KM-1, RT-3]
GV-1: [ID-7]
GV-2: [GV-1]
GV-3: [GV-1, GV-2, ID-4, GV-4]
GV-4: [ID-6, ID-7]
GV-5: [GV-1]
GV-6: [OB-1]
GV-7: [OB-1]
GV-8: [GV-1, GV-5]
GV-9: [OB-1, OB-2, GV-1, GV-5]
GV-10: [GV-8, OB-1]
ID-1: []
ID-2: []
ID-3: [ID-5, ID-6]
ID-4: []
ID-5: [ID-6]
ID-6: []
ID-7: [ID-6]
ID-8: [ID-2, ID-4, ID-5]
RT-1: [ID-4]
RT-2: [OB-2]
RT-3: [ID-7]
RT-4: [RT-8, ID-7]
RT-5: []
RT-6: [RT-5]
RT-7: [RT-8]
RT-8: [OB-1]
RT-9: []
RT-10: [RT-7, RT-8]
RT-11: [KM-1, KM-4, ID-4]
KM-1: [ID-2, ID-4]
KM-2: [ID-2]
KM-3: []
KM-4: []
KM-5: []
KM-6: []
KM-7: []
IN-1: [ID-6]
IN-2: []
IN-3: []
IN-4: [IN-1]
OB-1: []
OB-2: [GV-1, RT-8]
```

## Department Pattern Bundles

| Department | Key Patterns | Value Focus |
|---|---|---|
| Sales Agent | ID-2, ID-4, IN-2, KM-5, RT-5, RT-4 | Win rate improvement, deal cycle shortening, pipeline health |
| HR Agent | KM-4, KM-6, RT-4, GV-4, RT-6 | Recruitment efficiency, attrition prevention, inquiry self-service |
| Customer Support Agent | ID-1, RT-3, KM-1, RT-7, RT-9 | CSAT improvement, resolution efficiency, churn prevention |
| Engineering Agent | IN-1, ID-6, RT-8, OB-1, GV-9, ID-7 | Development productivity, faster incident response |
| Executive Agent | KM-3, KM-2, KM-6, GV-8, GV-7, OB-2 | Decision acceleration, enterprise optimization, early risk detection |

## Foundation Patterns (High Priority)

The following patterns are dependencies for many other patterns. Establish them first; retrofitting them later is costly.

| Pattern | Depended on by |
|---|---|
| OB-1 Observability Lake | GV-7, GV-9, GV-6, RT-8, GV-10 |
| OB-2 Unified Audit | GV-9 |
| ID-2 OBO | KM-1, KM-2, EX-1, EX-3 |
| ID-4 Permission Mirror | KM-1, RT-1, RT-11, GV-3, ID-8 |
| ID-6 Zero-Trust PDP/PEP | GV-4, ID-7, ID-5, IN-1, ID-3 |
| ID-7 Policy-as-Code | RT-3, RT-4, GV-4, GV-1 |
| GV-1 Control Plane | GV-2, GV-8, OB-2, GV-9 |
| RT-8 Durable Workflow | RT-4, RT-7, OB-2, RT-10 |

## Minimum Viable Governance (MVP)

Minimum configuration to deliver a read-only low-risk, high-frequency use case (knowledge search, meeting summary) to production within 30 days.

```
ID-2 (OBO read-only) + KM-1 (permission filter) + OB-1 (logging)
```

These three patterns enable running a read-only agent with audit trail (who accessed what). Build out the full governance stack in parallel.
