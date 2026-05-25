---
title: "TO-2 Central Data Lake vs. Federated Context Mesh"
description: "Decision criteria for building a knowledge base with a central vector DB or a federated Context Mesh."
status: done
---

# TO-2 Central Data Lake vs. Federated Context Mesh

## Overview

Indexing all internal documents in a central vector DB gives fast search. However, indexing data where viewing permissions vary per person — like Salesforce deal records — means permission changes cannot keep up, leading to incidents where "data that should not be visible is visible." Whether to choose a centralized lake or a federated Context Mesh ([KM-2](../../patterns/km-knowledge/km2-context-mesh.md)) — in practice a hybrid of "public information in the lake, confidential in the Mesh" is essential, and this covers how to draw that line.

## Comparison

| Perspective | Central Vector DB / Lake | Federated Context Mesh ([KM-2](../../patterns/km-knowledge/km2-context-mesh.md)) |
|---|---|---|
| Suitable for | Analytics, BI, statistics | AI context retrieval with permissions |
| Benefits | Fast, easy to aggregate | Easier to maintain permissions |
| Drawbacks | Millisecond permission sync is practically impossible → leakage | Latency, implementation complexity |

## Decision Criteria

- **Public information with no permission requirements** (company policies, public knowledge base) → Index in a central vector DB for fast retrieval
- **Confidential SaaS data** (personal Salesforce records, Workday information, etc.) → Federated Mesh with JIT retrieval using the individual's own token. Avoids permission synchronization problems
- **Even when pre-indexing**, ACL bundling ([KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md)) is mandatory

!!! danger "Indexing Confidential Data Just Because It's Fast — Forbidden"
    Indexing confidential data in a central vector DB means delays in reflecting permission changes lead directly to leakage. Never sacrifice permission guarantees for confidential data in the name of speed.

## Hybrid and Gradual Approach

Hybrid is essential. Retrieve public information quickly via the lake; retrieve confidential information via the Mesh while maintaining permissions. A practical configuration combines both, routing through [KM-3 Knowledge Graph](../../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md).

## Related Patterns

- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — ACL-bundled pre-indexing
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — the core federated retrieval design
- [KM-3 Canonical Object & Knowledge Graph](../../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) — unified routing
- [ID-2 Identity Federation & OBO](../../patterns/id-identity/id2-identity-federation-obo.md) — JIT retrieval using the individual's own token
