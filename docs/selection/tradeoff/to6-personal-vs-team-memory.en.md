---
title: "TO-6 Personal Memory vs. Project/Team Memory"
description: "Design guidance for physically and logically separating Personal Enclave and Project Workspace and aligning sharing scope with the org graph to prevent leakage and cross-contamination."
status: done
---

# TO-6 Personal Memory vs. Project/Team Memory

## Overview

It's convenient when an agent remembers "the approach that person taught me last time." But what if someone transfers to a different team, and the original team's agent can still access that person's work notes? Personal memory used for individual efficiency and project knowledge shared across a team must be physically and logically separated — otherwise they become a breeding ground for leakage and cross-contamination.

## Comparison

| Perspective | Personal Enclave (Personal Domain) | Project Workspace (Shared Domain) |
|---|---|---|
| Ownership | Individual | Project, team, department |
| Who Can Access | Only the individual | Project members |
| Contains | Personal settings, personal notes, work style, confidential information | Shared knowledge, work history, project documents |
| Management Pattern | [KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) | [RT-11](../../patterns/rt-runtime/rt11-project-digital-twin.md) |
| Separation Method | Physical separation (separate storage) or strong logical separation | ACL following org graph |

## Decision Criteria

Personal memory is needed for individual efficiency; shared memory is needed to prevent silos. But managing both in the same store creates the risk of personal confidential information leaking into the project shared domain.

The baseline is **Physical or logical separation of Personal Enclave and Project Workspace** ([KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) / [RT-11](../../patterns/rt-runtime/rt11-project-digital-twin.md)).

Criteria for determining shared scope:

- **Follow the org graph**: Who are the project members should be obtained from the authorization management system (IdP, HR system). Neither agents nor users should be able to arbitrarily change the scope.
- **Conduct inventory at project completion**: After a project ends, explicitly decide whether to retain, archive, or delete information remaining in the shared domain.
- **Personal information must not be written to the shared domain**: Even if documents about personal performance evaluations, salary information, or medical information are created as project documents, they must not enter the shared domain.

Anti-patterns from consolidation:

- Confidential items written as personal notes become visible to all team members
- Memories from multiple projects become mixed, and the agent uses incorrect project information in responses
- Resigned employees' personal memory persists in the organization's shared store

## Hybrid and Gradual Approach

The ideal is a system where memories are written to the appropriate scope without users being aware of it.

1. First implement only the Personal Enclave and retain all memories in personal scope.
2. Add Project Workspace per project, allowing memory to move from personal to shared only through an explicit "share" operation.
3. Establish org graph synchronization ([ID-8](../../patterns/id-identity/id8-consent-access-transparency.md)) so that membership changes are automatically reflected in access rights.
4. Set memory expiration periods ([KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) TTL) to prevent old information from continuing to accumulate.

## Related Patterns

- [KM-4 Scoped Memory Hierarchy](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)
- [RT-11 Project Digital Twin](../../patterns/rt-runtime/rt11-project-digital-twin.md)
- [ID-8 Consent & Access Transparency](../../patterns/id-identity/id8-consent-access-transparency.md)
