---
title: "GV-9 Incident Response & Kill Switch"
description: "Pre-built mechanisms for detection, granular shutdown, trace preservation, impact assessment, notification, remediation, and post-mortem in response to mis-sends, leaks, and runaway behavior."
status: done
---

# GV-9 Incident Response & Kill Switch

## Overview

When an agent causes a problem in production, having only two options — "stop everything" or "do nothing" — is the worst possible state. This pattern pre-builds a Kill Switch capable of instantly stopping at the granularity of model, agent, tool, or tenant, along with a full incident response flow: detect → contain → preserve traces → assess impact → notify → remediate → post-mortem. "Can stop it, can investigate it, knows the scope" are the minimum requirements for production operation.

## Enterprise Problem Solved

When agents run in production, incidents will occur. Accidental transmission of confidential data, unauthorized manipulation via prompt injection, unintended data overwrites due to runaway tools, cost explosions — facing these with no way to stop them, no way to understand what happened, and no way to identify the scope of impact represents the greatest risk in embedding AI into core business operations. A design with only full shutdown capability means one agent's problem stops all AI across the enterprise. Organizations without granular stop capability are forced into a binary choice at incident time: shut everything down or leave it running.

!!! tip "Minimum Viable Requirements (MVP)"
    Prepare one Kill Switch that can instantly stop at the agent level (feature flag or Gateway blocklist), and write a Runbook covering stop → notify → root cause investigation. Granularity refinement and replay capabilities can be added later.

## Value Hypothesis

Instant shutdown and rapid recovery at failure time minimizes business downtime caused by agents. The existence of a safety net makes it possible to apply agents to higher-risk operations, expanding the scope of automation (= the total value generated).

## Solution and Design

Incident response proceeds through the following flow.

```mermaid
flowchart LR
    DET[Detect<br/>Anomaly Detection / Alert] --> CONT[Contain<br/>Granular Shutdown]
    CONT --> PRES[Preserve Traces<br/>Audit Snapshot]
    PRES --> ASSESS[Impact Assessment<br/>Scope Identification]
    ASSESS --> NOTIFY[Notify<br/>Stakeholders / Management]
    NOTIFY --> FIX[Remediate<br/>Root Cause Fix / Rollback]
    FIX --> PM[Post-Mortem<br/>Recurrence Prevention]
```

Design shutdown granularity as follows.

| Shutdown Granularity | Target | Example |
|---|---|---|
| Model | Block a specific model version | Quality degradation detected in new version |
| Agent | Stop a specific agent | Malfunctioning department agent |
| Tool | Disable a specific tool/MCP | Connector with leaked API key |
| Tenant | Stop a specific department/project | Department with cost explosion |
| Global | Emergency stop all agents | Critical security incident |

## Fit / Not a Fit

| Fit | Not a Fit |
|---|---|
| Required for all production AI | — |
| There are essentially no cases where this is not a fit | Kill Switch design cost is extremely small compared to operational risk |

## Component Technologies and System Integrations

- **Instant shutdown**: Kill Switch, Circuit Breaker
- **Operational procedures**: Runbooks (automatable procedures)
- **Evidence preservation**: Audit Snapshot, Event Store
- **Reproduction**: Replay Tool (reproducing past executions)
- **Access revocation**: Access Revocation (immediate expiration of tokens and keys)
- **Monitoring integration**: SIEM (Splunk / Sentinel), PagerDuty

## Pitfalls / Selection Considerations

!!! danger "Designing with Only Global Shutdown"
    Having only global shutdown means one agent's problem stops all AI across the enterprise. Design the system to allow granular stopping by model, agent, tool, and tenant.

- A Kill Switch is not useful just by "existing" — verify its operation through regular game-day exercises.
- Automate trace preservation during incidents. Manual response is too slow and evidence disappears.
- Feed post-mortem findings back into policies ([ID-7](../id-identity/id7-policy-as-code-guardrail.md)) and evaluation ([GV-7](gv7-evaluation-governance-pipeline.md)) to structurally prevent recurrence.

## Related Patterns

- [GV-1 Agent Control Plane](gv1-agent-control-plane.md) — Complement: handles permission management for per-agent shutdown control
- [GV-5 Central Model Gateway](gv5-central-model-gateway.md) — Complement: executes model-level blocking at the Gateway
- [OB-1 Observability Lake](../ob-observability/ob1-observability-lake.md) — Complement: accumulates trace data needed for failure investigation
- [OB-2 Unified Audit & Lineage](../ob-observability/ob2-unified-audit-lineage.md) — Complement: used for impact scope identification and replay during incidents
- [GV-6 Version Registry](gv6-version-registry.md) — Complement: used to identify rollback target versions and perform reversion
