---
title: "DC-2 Timeout, Retry, and Budget (Cost Ceiling)"
description: "A continuous parameter for setting agent timeout, retry count, and session cost ceiling."
status: done
---

# DC-2 Timeout, Retry, and Budget (Cost Ceiling)

## Overview

Compared to traditional APIs, agents are orders of magnitude slower, and a single session can consume hundreds of dollars in token costs. If timeout is set too short, legitimate processing is aborted prematurely; if too loose, infinite loops generate enormous bills. This covers how to set three limits: "how many seconds to wait," "how many times to retry," and "how much can be spent per session."

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (too strict) | Timeout too short, no retry allowed, budget too small | Legitimate processing is cut off midway, reducing task completion rates |
| Too much (too permissive) | Timeout too long, unlimited retries, no budget ceiling | Infinite loops or runaway behavior generates enormous bills and resource occupation |

## Decision Criteria

- **Timeout**: Set TTFT (Time to First Token) and overall timeout (no-progress time) separately. TTFT is for determining if the model is responsive; overall timeout is for determining if processing is progressing
- **Retry**: Only retry idempotent steps. Limit to 2–3 retries maximum with exponential backoff and jitter. Retrying non-idempotent operations (writes, transmissions) carries a high risk of double execution
- **Session budget**: Set ceilings on both cost (token consumption amount) and time (elapsed time). Subordinate each step's budget to the overall session budget
- **Multi-agent configuration**: In [RT-2 RACI-based Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md) setups, inference cost multiplies by N, so budget ceilings must be strict

## Adjustment Mechanism

- Measure per-session cost, elapsed time, retry count, and timeout occurrence rate using [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md)
- Link to department-level budgets in [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) and define behavior when budget is exceeded (stop, degrade, escalate for approval)
- Consider task splitting or async processing ([RT-8](../../patterns/rt-runtime/rt8-durable-workflow.md)) for processes with high timeout rates

## Related Patterns

- [RT-2 RACI-based Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md) — cost increase in multi-agent setups
- [RT-8 Durable Workflow](../../patterns/rt-runtime/rt8-durable-workflow.md) — handling long-running processes that exceed timeout
- [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) — budget management and allocation
- [GV-9 Incident Response & Kill Switch](../../patterns/gv-governance/gv9-incident-response-kill-switch.md) — forced stop during runaway behavior
