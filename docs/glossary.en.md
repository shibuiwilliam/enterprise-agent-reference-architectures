---
title: "Glossary"
description: "Definitions of specialized terms and abbreviations used throughout this site."
---

# Glossary

Definitions of the major specialized terms used throughout this site. Terms link back here from their first occurrence in each pattern page.

| Term | Definition |
|---|---|
| **OBO (On-Behalf-Of)** | A delegation method using OAuth 2.0 Token Exchange (RFC 8693) or similar to call downstream services with a token reduced to the requester's own permissions. → [ID-2](patterns/id-identity/id2-identity-federation-obo.md) |
| **Confused Deputy** | A security issue where an authorized principal executes a request from an unauthorized principal using its own authority. Occurs when an agent performs proxy operations on behalf of a user using excessive service account permissions. → [ID-2](patterns/id-identity/id2-identity-federation-obo.md) |
| **Mosaic Effect** | A phenomenon where individually non-confidential data, when combined, makes confidential information inferable. Example: seating chart + travel records + registration info → inference of an undisclosed M&A contact. → [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **Permission Mirror** | A cache that synchronizes each SaaS system's permissions (ACLs/roles/groups) to the agent platform side. Not an authoritative source but a supplement to SaaS-native authorization. → [ID-4](patterns/id-identity/id4-permission-mirror-least-of.md) |
| **Zanzibar** | A relationship-based access control (ReBAC) system developed by Google. Expresses permissions as relationship tuples such as "User X is a viewer of Document Y." OSS implementations include SpiceDB and OpenFGA. → [ID-4](patterns/id-identity/id4-permission-mirror-least-of.md), [ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md) |
| **ReBAC (Relationship-Based Access Control)** | A model that controls access based on relationships between resources (owner, member, viewer, etc.). Used in combination with RBAC (role-based) and ABAC (attribute-based). → [ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md) |
| **PDP / PEP** | Policy Decision Point / Policy Enforcement Point. A design that separates the authorization decision logic (PDP) from the gate that applies those decisions at runtime (PEP). → [ID-6](patterns/id-identity/id6-zero-trust-pdp-pep.md) |
| **DPA (Data Processing Agreement)** | A data processing agreement that contractually obligates an LLM vendor to prohibit using input data for training, delete data after processing, etc. → [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **TEE (Trusted Execution Environment)** | An execution environment that encrypts and isolates memory at the hardware level, preventing even host OS or administrators from reading data. Includes Confidential VMs and NVIDIA Confidential GPUs. → [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **Zeroization** | The process of clearing a memory region in a cryptographically secure manner to prevent data residue. Applied at session termination in ephemeral contexts. → [KM-7](patterns/km-knowledge/km7-ephemeral-secure-context-bus.md) |
| **SoR (System of Record)** | The system holding the authoritative master of business data. Examples: Salesforce (CRM), Workday (HCM), ServiceNow (ITSM). Agent write boundaries are designed with protection of SoR integrity in mind. → [RT-6](patterns/rt-runtime/rt6-sor-write-boundary.md) |
| **Saga** | A pattern for decomposing distributed transactions into a series of local transactions and compensating operations. Ensures rollback on partial failure when agents operate across multiple SaaS systems. → [RT-7](patterns/rt-runtime/rt7-enterprise-saga.md) |
| **RACI** | A matrix defining responsibility allocation with four roles: Responsible (executor), Accountable (responsible party), Consulted (advisors), and Informed (notified parties). → [RT-2](patterns/rt-runtime/rt2-raci-multi-agent.md) |
| **GraphRAG** | A RAG method combining knowledge graphs and vector search. Strong for relational queries about entities ("Why was this design decision made?"). → [KM-3](patterns/km-knowledge/km3-canonical-object-knowledge-graph.md), [RT-11](patterns/rt-runtime/rt11-project-digital-twin.md) |
| **MCP (Model Context Protocol)** | A protocol standardizing connections between LLMs and tools/data sources. Functions as a common interface when agents call external systems. → [IN-1](patterns/in-integration/in1-tool-mcp-gateway.md) |
| **OPA (Open Policy Agent)** | A general-purpose policy engine. Writes policies in the Rego language to perform unified authorization decisions for APIs, Kubernetes, data access, etc. → [ID-7](patterns/id-identity/id7-policy-as-code-guardrail.md) |
| **Cedar** | A policy language and evaluation engine developed by AWS. Describes fine-grained authorization using Permit/Forbid rules. Used in Amazon Verified Permissions. → [ID-7](patterns/id-identity/id7-policy-as-code-guardrail.md) |
