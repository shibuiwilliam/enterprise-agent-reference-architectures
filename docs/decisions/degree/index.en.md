---
title: "Degree Selection Criteria"
description: "How to set continuous parameters such as autonomy tier, budget, log granularity, context volume, memory retention, and guardrail strength."
status: done
---

# Degree Selection Criteria

Continuous parameters cause harm at both extremes — too small and too large. The following provides starting points and decision axes, on the premise that continuous adjustment is performed based on production traces ([OB-1](../../patterns/ob-observability/ob1-observability-lake.md)) and evaluation ([GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)).

| ID | Name | Overview |
|---|---|---|
| [DC-1](dc1-risk-tier-boundary.md) | Autonomy Tier Boundary | How to draw Risk-Tier lines. Determined by irreversibility of impact, amount, sensitivity, and job responsibility |
| [DC-2](dc2-timeout-retry-budget.md) | Timeout, Retry, and Budget | Cost ceiling. Setting budget constraints for slow, high-cost agents |
| [DC-3](dc3-log-granularity.md) | Log Granularity | Three-layer separation. Differentiating storage destinations and granularity for meta, body, and aggregate layers |
| [DC-4](dc4-context-volume.md) | Context Volume | top-k and token budget. Narrowing down to the minimum data necessary for the purpose |
| [DC-5](dc5-memory-retention.md) | Memory Retention and Forgetting | TTL and scope. Selecting based on importance × freshness × reference frequency |
| [DC-6](dc6-guardrail-strength.md) | Guardrail Strength | False positives vs. false negatives. Making thresholds variable per risk pathway |
| [DC-7](dc7-cache-jit-ttl.md) | Cache Aggressiveness and JIT Credential TTL | Tuning the tradeoff between incorrect cache hits and speed |
| [DC-8](dc8-model-routing.md) | Model Strength and Data-Classification-Based Routing | Routing by difficulty and data classification |
| [DC-9](dc9-canary-event-throttle.md) | Canary Stages and Event-Driven Frequency Limits | Multi-stage rollout and event storm suppression |
