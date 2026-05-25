---
title: "DC-4 Context Volume (top-k and Token Budget)"
description: "A continuous parameter for minimizing the context injected into prompts from RAG and similar retrieval, constrained by purpose."
status: done
---

# DC-4 Context Volume (top-k and Token Budget)

## Overview

Just because 50 internal documents were retrieved with RAG does not mean stuffing them all into the prompt improves accuracy. Beyond high token consumption and increased latency, the "lost in the middle" phenomenon — where information in the middle of a long context is ignored — can actually reduce answer quality. This covers how to set top-k and token budgets to narrow down to "the minimum data necessary for this task" rather than "data that can be used" ([KM-5 Purpose-Bound Context](../../patterns/km-knowledge/km5-purpose-bound-context.md)).

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (too few) | top-k too small, relevant context missing | Answer quality degrades and hallucinations increase |
| Too much (too many) | All retrievable data injected in full | Quality degradation (lost in the middle), cost increase, latency degradation, and unnecessary spread of confidential information |

## Decision Criteria

- Select only the top-ranked results by relevance, and further reduce count with a reranker
- Set a per-purpose token budget and compress within that budget. Required volume differs by task type (Q&A, summarization, analysis)
- Follow the purpose-bound principle of [KM-5](../../patterns/km-knowledge/km5-purpose-bound-context.md) and do not inject attributes or fields unnecessary for the task
- Mask high-sensitivity information with [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) before injection

## Adjustment Mechanism

- Measure correlation between answer quality and injection volume using [GV-7 Evaluation Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)
- Find the optimal point via A/B testing with varied top-k and token budget values
- Monitor trends in token consumption and quality scores with [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) and track cost-to-quality ratio

## Related Patterns

- [KM-5 Purpose-Bound Context](../../patterns/km-knowledge/km5-purpose-bound-context.md) — the purpose-bound principle
- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — context retrieval in access-controlled RAG
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — context volume control in federated retrieval
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — masking before injection
