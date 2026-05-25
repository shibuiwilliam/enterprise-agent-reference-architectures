---
title: "DC-7 Cache Aggressiveness and JIT Credential TTL"
description: "A continuous parameter for adjusting search cache and JIT credential TTL based on use case risk."
status: done
---

# DC-7 Cache Aggressiveness and JIT Credential TTL

## Overview

When ten people ask the same question in a row, running full inference every time wastes cost. But immediately after an HR transfer, returning "this person's list of direct reports" from cache would return results based on an outdated org chart. Similarly, extending the validity of JIT-issued temporary authentication tokens ([ID-5](../../patterns/id-identity/id5-jit-scoped-credentials.md)) reduces re-authentication burden, but creates the risk that access persists after permissions are revoked. This covers how to adjust cache aggressiveness and credential TTL based on the risk of each use case.

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (too conservative, TTL too short) | No cache, credentials expire immediately | Every query triggers search or authentication, increasing latency. High-cost JIT credential re-issuance causes bottlenecks |
| Too much (too aggressive, TTL too long) | Cache retained broadly and for long periods | Continues serving old search results. JIT credentials remain valid after resignation or permission changes, creating permission excess risk |

## Decision Criteria

Cache and credential TTL must be set individually based on the risk characteristics of each use case.

**Search Cache**

- Use exact-match cache as primary and semantic cache as secondary
- For high-risk domains (searches containing confidential information, operations with side effects): set a high similarity threshold and short TTL
- Disable caching for personalized responses, time-series-dependent data, and retrieval results containing confidential information — always fetch fresh data

**JIT Credential TTL**

- Separate TTL by use case risk from [ID-5](../../patterns/id-identity/id5-jit-scoped-credentials.md). Short TTL (minutes) for sensitive data access or operations with side effects; relatively longer TTL (hours) for lightweight read-only operations
- Provide a mechanism to forcibly expire credentials before TTL expiration when permission changes, resignations, or session termination are detected

!!! tip "Aligning Cache with Least Privilege"
    When cache retains an old permission state, it undermines the least-privilege effect achieved through [ID-4 Permission Mirror & Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md). Synchronize cache invalidation with permission change events.

## Adjustment Mechanism

- Measure cache hit rate, miss rate, and TTL expiration occurrence rate using [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md)
- For paths with low cache hit rate, consider extending TTL or relaxing similarity thresholds; for paths with high hit rate, periodically verify content freshness requirements
- Alert when JIT credential residuals are detected and build an automatic expiration mechanism

## Related Patterns

- [ID-5 JIT Scoped Credentials](../../patterns/id-identity/id5-jit-scoped-credentials.md) — the core temporary credential issuance and expiration design
- [ID-4 Permission Mirror & Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md) — alignment with least privilege
- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — cache design in access-controlled RAG
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — cache layer in federated retrieval
