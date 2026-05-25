---
title: "DC-5 Memory Retention and Forgetting (TTL and Scope)"
description: "A continuous parameter for deciding how long agent memory is retained and when to forget it, using TTL, scope, and lifecycle rules."
status: done
---

# DC-5 Memory Retention and Forgetting (TTL and Scope)

## Overview

An agent that remembers "how to do things from the last conversation" enables personalization, but holding on indefinitely to work records of former employees or confidential memos from completed projects becomes a mass of leakage risk. This covers how to design "what to remember for how long" and "when to forget it" per scope — session, individual, project, organization ([KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)).

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
