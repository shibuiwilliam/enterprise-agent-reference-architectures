---
title: "DC-9 Canary Stages and Event-Driven Frequency Limits"
description: "A continuous parameter for designing canary release stages and frequency limits for event-driven agents."
status: done
---

# DC-9 Canary Stages and Event-Driven Frequency Limits

## Overview

A prompt improvement is ready for company-wide rollout — but applying it to all users at once risks company-wide impact if quality degrades. When thousands of events fire simultaneously during month-end closing, agents can go into an inference storm that causes costs to spike. This covers how to design the stages of canary releases (1% → 5% → 25% → 100%) and frequency limits for event-driven agents ([RT-10](../../patterns/rt-runtime/rt10-event-driven-orchestrator.md)).

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-9
parameter: canary_event_throttle
rules:
  - condition: "new_agent_version_deploy == true"
    canary_stages: [1, 5, 25, 100]
    stage_unit: percent_of_traffic
    reason: "Use 1%→5%→25%→100% multi-stage rollout as baseline; collect sufficient traffic at each stage before advancing"
  - condition: "canary_stage_healthy == false"
    action: auto_rollback_via_gv6
    reason: "If quality score, error rate, or cost exceeds threshold at any canary stage, trigger GV-6 automatic rollback immediately"
  - condition: "latency_sensitive == false AND eval_complete == false"
    action: supplement_with_offline_eval
    reason: "When live traffic is insufficient for statistical significance, supplement with offline evaluation (GV-7) before advancing to next stage"
  - condition: "event_volume_exceeds_budget == true"
    throttle_action: queue_or_sample
    mechanisms: [debounce, rate_limit, session_budget_cap]
    reason: "Combine debounce, rate limit, and session budget cap to prevent event storms from causing cost spikes and downstream overload"
  - condition: "throttle_causing_stale_state == true"
    action: loosen_throttle_per_event_type
    reason: "Over-throttling causes agents to operate on stale state; tune throttle parameters per event type based on business criticality and inference cost"
```

## Harms of Too Little or Too Much

**Canary Release**

| Extreme | State | Harm |
|---|---|---|
| Too little (too fine-grained, too slow) | Incrementing 1% → 2% → 3%… | New version deployment takes too long; small sample sizes fail to yield statistically significant differences |
| Too much (too coarse, too fast) | Rolling out to 50%+ from the first stage | Impact spreads before problems are detected; rollback cost becomes high |

**Event Frequency Limits**

| Extreme | State | Harm |
|---|---|---|
| Too little (no limits) | All events delivered to agents immediately | Event storms occur, causing inference costs to spike. Dependent systems also become overloaded |
| Too much (too strict) | Most events throttled | Necessary events are lost, and agents continue making decisions based on stale state |

## Decision Criteria

**Canary Release Stage Design**

- Use 1% → 5% → 25% → 100% multi-stage as the base, collecting sufficient traffic at each stage before proceeding
- Trigger automatic rollback from [GV-6 Version Registry & Rollback](../../patterns/gv-governance/gv6-version-registry.md) at any stage where quality score, cost, or error rate falls below threshold
- When traffic is low and statistically significant differences are difficult to obtain, use offline evaluation ([GV-7 Evaluation Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)) as supplementary data before deciding to advance to the next stage

**Event-Driven Frequency Limits**

- Combine three mechanisms: debounce (aggregating events that fire in rapid succession), frequency cap (maximum processing count per unit time), and budget cap (maximum session budget consumption)
- During event storms with large volumes of events from a single source, queue excess events that exceed the frequency cap, or thin them out with sampling
- Set frequency limit parameters per event type, considering business importance and inference cost

## Adjustment Mechanism

- Link with deployment status in [GV-6 Version Registry & Rollback](../../patterns/gv-governance/gv6-version-registry.md) to automatically collect and evaluate quality metrics at each stage
- Use offline evaluation from [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) to supplement decision-making at stages with low production traffic
- Measure event processing volume, skip volume, and error rates with [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) to detect excess or deficiency in frequency limit parameters
- Analyze event storm occurrence patterns and adjust debounce time windows and frequency caps to align with business cycles (daily batches, month-end closing, etc.)

## Related Patterns

- [GV-6 Version Registry & Rollback](../../patterns/gv-governance/gv6-version-registry.md) — the core canary deployment and automatic rollback implementation
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — supplementing canary decisions with offline evaluation
- [RT-10 Event-Driven Orchestrator](../../patterns/rt-runtime/rt10-event-driven-orchestrator.md) — execution control for event-driven agents
