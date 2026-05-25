---
title: "Tradeoff Selection Criteria"
description: "Decision criteria for 12 binary choice axes in enterprises: OBO vs. service account, central lake vs. Mesh, Copilot vs. Autopilot, and more."
status: done
---

# Tradeoff Selection Criteria

Most apparent binary oppositions come down to "where to draw the line." The following presents 12 decisive axes in enterprise settings. Each axis consists of a comparison table, decision criteria, a hybrid approach, and related patterns — providing conditional selection criteria rather than abstract judgments of superiority.

| ID | Name | Overview |
|---|---|---|
| [TO-1](to1-obo-vs-service-account.md) | OBO Delegation vs. Service Account | Determining usage based on three axes: permission fidelity, audit attribution, and implementation cost |
| [TO-2](to2-lake-vs-mesh.md) | Central Data Lake vs. Federated Context Mesh | Splitting index strategy by data type and permission management method |
| [TO-3](to3-single-vs-multi-agent.md) | Single Agent vs. RACI Multi-Agent | The basis for multi-agent is "because enterprise responsibility division spans multiple parties" — not "because it's complex" |
| [TO-4](to4-readonly-vs-write.md) | Read-only vs. Write-capable (Gradual Expansion) | Clearly separate read and write operations and gradually expand permissions |
| [TO-5](to5-copilot-vs-autopilot.md) | Copilot vs. Autopilot | Clearly separate write APIs with HitL Copilot and read APIs with Autopilot |
| [TO-6](to6-personal-vs-team-memory.md) | Personal Memory vs. Project/Team Memory | Physically and logically separate personal and shared domains to prevent cross-contamination |
| [TO-7](to7-full-vs-selective-log.md) | Full Prompt Log vs. Selective Trace Log | Balancing cost, confidentiality, and reproducibility with three-layer separation |
| [TO-8](to8-central-vs-federation.md) | Central Platform vs. Department Federation | Two-layer governance where guardrails are central and business logic belongs to departments |
| [TO-9](to9-custom-vs-ipaas.md) | Custom Connector Build vs. Existing iPaaS Reuse | Verify authorization granularity of existing assets; MCP-ify only what's insufficient |
| [TO-10](to10-onprem-vs-external.md) | Internal/On-premises Model vs. External API | Auto-routing inference paths by data classification |
| [TO-11](to11-sync-vs-async.md) | Synchronous vs. Asynchronous | Selecting processing method based on processing time and presence of approval flows |
| [TO-12](to12-prompt-vs-platform.md) | Guard with Prompts vs. Guard with Policy/Platform | Safety boundaries must always be on the execution platform side |
