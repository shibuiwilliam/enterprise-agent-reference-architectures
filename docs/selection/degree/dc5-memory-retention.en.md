---
title: "DC-5 Memory Retention and Forgetting (TTL and Scope)"
description: "A continuous parameter for deciding how long agent memory is retained and when to forget it, using TTL, scope, and lifecycle rules."
status: done
---

# DC-5 Memory Retention and Forgetting (TTL and Scope)

## Overview

An agent that remembers "how to do things from the last conversation" enables personalization, but holding on indefinitely to work records of former employees or confidential memos from completed projects becomes a mass of leakage risk. This covers how to design "what to remember for how long" and "when to forget it" per scope — session, individual, project, organization ([KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)).

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-5
parameter: memory_retention_ttl
rules:
  - condition: "memory_scope == 'session'"
    ttl: session_end
    reason: "Session-scoped memory is discarded at session end; temporary working context does not require persistence"
  - condition: "memory_scope == 'personal' AND reference_frequency IN ['high', 'medium']"
    ttl: 90_days_rolling_with_extension
    reason: "Actively-used personal memory (preferences, work style) warrants multi-month retention with TTL extension on access"
  - condition: "memory_scope == 'personal' AND reference_frequency == 'never'"
    action: auto_archive_then_delete
    ttl: 30_days_after_last_access
    reason: "Unreferenced personal memory should be auto-archived and deleted; stale data accumulates risk without value"
  - condition: "lifecycle_event IN ['employee_departure', 'role_change', 'project_end']"
    action: immediate_expiry_and_permission_revocation
    reason: "HR lifecycle events (departure, transfer, project end) must trigger immediate memory expiry and access revocation"
  - condition: "permission_change_event == true"
    action: immediate_delete_all_personal_scope
    reason: "Right-to-erasure: individual must be able to delete or modify their personal memory scope at any time (ID-8)"
```

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (forgets quickly) | All cleared at session end | The same explanation is needed every time, and the value of personalization disappears |
| Too much (remembers everything) | All memory retained indefinitely | Incorrect judgments based on outdated information, residual data from resigned employees, increased storage costs |

## Decision Criteria

- Select what to retain based on three axes: **importance × freshness × reference frequency**. Compress old details into summaries
- Set TTL and expiration conditions per scope in [KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) (session, individual, project, organization)
- **Link to lifecycle events**: Expire memory and permissions when projects end, employees resign, or transfer
- **Right to erasure**: Include in the design the right for individuals to delete or modify their own memory ([ID-8](../../patterns/id-identity/id8-consent-access-transparency.md))

## Adjustment Mechanism

- Measure memory reference frequency and freshness with [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) and auto-archive or delete unreferenced memory
- Implement auto-expiration of unnecessary memory in conjunction with HR system events (transfers, resignations)
- Evaluate correlation between memory volume and task quality with [GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) and adjust retention policies

## Related Patterns

- [KM-4 Scoped Memory Hierarchy](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) — the core scoped memory hierarchy design
- [ID-8 Consent & Access Transparency](../../patterns/id-identity/id8-consent-access-transparency.md) — right to erasure and transparency principles
- [RT-11 Project Digital Twin](../../patterns/rt-runtime/rt11-project-digital-twin.md) — memory management at project scope
- [TO-6 Personal Memory vs. Project/Team Memory](../tradeoff/to6-personal-vs-team-memory.md) — decision axis between individual vs. shared
