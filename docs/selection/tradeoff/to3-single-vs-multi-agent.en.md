---
title: "TO-3 Single Agent vs. RACI Multi-Agent"
description: "Selection guidance establishing that the only legitimate basis for multi-agent is 'because responsibility allocation in the enterprise spans multiple parties' — not 'because it's complex.'"
status: done
---

# TO-3 Single Agent vs. RACI Multi-Agent

## Overview

"Let's go multi-agent because the processing is complex" is the entry point to over-engineering in enterprise settings. Going multi means costs multiply by N, latency adds up, and failure points increase. Multi-agent is justified not "because it's technically complex" but only "because enterprise responsibility allocation spans multiple departments like sales, legal, and finance."

## Comparison

| Perspective | Single Agent | RACI Multi-Agent ([RT-2](../../patterns/rt-runtime/rt2-raci-multi-agent.md)) |
|---|---|---|
| Implementation Cost | Low | High (orchestration and communication infrastructure required) |
| Latency | Low | High (inter-agent coordination costs add up) |
| Failure Points | Few | Many (each agent and communication path is a failure point) |
| Clarity of Responsibility | Concentrated at one point | Roles can be separated with RACI |
| Suitable For | Simple Q&A, low latency, low cost | Multi-department involvement, specialization, high-accountability tasks |

## Decision Criteria

**Start with a single agent.** The decision criterion for going multi is not "because the processing is complex." The only legitimate criterion is "**because enterprise responsibility allocation spans multiple departments and roles**" ([RT-2](../../patterns/rt-runtime/rt2-raci-multi-agent.md)).

Conditions where multi-agent is appropriate:

- Multiple departments are involved, and each has independent approval and accountability
- Sub-tasks with different specializations exist, each requiring a different model and toolset
- Accountability for final approval is clearly separated, and a single agent would make attribution ambiguous

Conditions where a single agent should be maintained:

- Even if processing is complex, if the responsible party is confined to one department or role
- When latency or availability requirements are strict and the overhead of distributed processing cannot be tolerated
- When the team lacks multi-agent operations experience and the cost of handling failures is unpredictable

## Hybrid and Gradual Approach

A realistic approach is to operate as a single agent, observe bottlenecks and points of responsibility division, and cut out only necessary parts incrementally.

1. Build a prototype as a single agent and identify business flows where responsibility boundaries emerge.
2. Only separate into sub-agents the parts where responsibility allocation has become clear.
3. Complete the multi-agent setup after building out the orchestrator ([RT-1](../../patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md)) and cost/quota management ([GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)).

## Related Patterns

- [RT-2 RACI Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md)
- [RT-1 Org-Hierarchical Hub-and-Spoke](../../patterns/rt-runtime/rt1-org-hierarchical-hub-spoke.md)
- [GV-8 Cost / Quota / Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md)
