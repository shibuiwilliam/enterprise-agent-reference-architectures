---
title: "TO-3 Single Agent vs. RACI Multi-Agent"
description: "Selection guidance establishing that the only legitimate basis for multi-agent is 'because responsibility allocation in the enterprise spans multiple parties' — not 'because it's complex.'"
status: done
---

# TO-3 Single Agent vs. RACI Multi-Agent

## Overview

"Let's go multi-agent because the processing is complex" is the entry point to over-engineering in enterprise settings. Going multi means costs multiply by N, latency adds up, and failure points increase. Multi-agent is justified not "because it's technically complex" but only "because enterprise responsibility allocation spans multiple departments like sales, legal, and finance."

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-3
decision_rules:
  - condition: "responsibility_spans_multiple_departments == false AND latency_sensitive == true"
    recommendation: single_agent
    reason: "Default to single agent; multi-agent adds cost, latency, and failure points without organizational benefit when responsibility is unified"
  - condition: "multiple_departments_with_independent_approval == true"
    recommendation: multi_agent
    reason: "Independent approval and accountability across departments (e.g. sales, legal, finance) justifies multi-agent RACI separation"
  - condition: "subtasks_require_different_models_or_toolsets == true"
    recommendation: multi_agent
    reason: "Specialist subagents with domain-specific models/tools are appropriate when subtasks have distinct expertise requirements"
  - condition: "team_multi_agent_experience == 'low' OR availability_requirements == 'strict'"
    recommendation: single_agent
    reason: "Low team experience or strict availability requirements make multi-agent operational overhead unacceptable"
  - condition: "single_agent_bottleneck_identified == true AND responsibility_split_boundary_clear == true"
    recommendation: multi_agent
    reason: "Incrementally extract only the subagent where a clear responsibility boundary has been observed in production"
```

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
