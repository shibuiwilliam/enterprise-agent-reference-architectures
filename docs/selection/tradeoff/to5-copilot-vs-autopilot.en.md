---
title: "TO-5 Copilot vs. Autopilot"
description: "Guidance to clearly separate read APIs as Autopilot and write APIs as HitL Copilot, and to advance Autopilot expansion gradually from domains where eval, canary, and audit are in place."
status: done
---

# TO-5 Copilot vs. Autopilot

## Overview

Executives often think "let the agent handle all the work and cut headcount." But when a probabilistically operating LLM starts autonomously rewriting Workday payroll data or SAP purchase orders, a single error can be irreversible. "Searching for information and suggesting" (Copilot) and "deciding and completing execution" (Autopilot) should be clearly separated, with the dividing line drawn at "read vs. write."

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-5
decision_rules:
  - condition: "operation_type == 'read_only' AND eval_complete == true AND canary_passed == true"
    recommendation: autopilot
    reason: "Read-only operations with no irreversible side effects and completed eval/canary validation are safe for autonomous execution"
  - condition: "operation_type IN ['update', 'delete', 'approve'] OR target_system IN ['erp', 'crm', 'hr']"
    recommendation: copilot
    reason: "Irreversible operations and writes to core business systems must retain human-in-the-loop via approval chain"
  - condition: "approval_rate_historically_high == true AND risk_level == 'low' AND kill_switch_available == true"
    recommendation: autopilot
    reason: "Operations that humans historically approve almost always, combined with kill switch and audit trail, are candidates for autopilot promotion"
  - condition: "infrastructure_readiness == 'incomplete' OR autopilot_expansion_too_fast == true"
    recommendation: copilot
    reason: "'Autopilot before readiness' is the primary risk; always start with Copilot and expand incrementally"
  - condition: "same_agent_mixed_operations == true"
    recommendation: hybrid_per_operation
    reason: "Within the same agent, apply Copilot/Autopilot per operation type; do not force a single mode across all operations"
```

## Comparison

| Perspective | Copilot (Work Assistance) | Autopilot (Work Proxy) |
|---|---|---|
| Human Involvement | Proposal, confirmation, and final approval required | Autonomous execution. Human involvement only for exceptions |
| Suitable For | Write APIs, high-risk operations, irreversible operations | Read APIs, low-risk operations, reversible operations |
| Impact on Failure | Minimized because humans block | Incorrect automated operations result in damage directly |
| Required Infrastructure | Approval flow ([RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)) | Eval, canary, audit trail, kill switch |
| ROI Realization Speed | Slow (human bottleneck) | Fast (but accident risk when infrastructure is insufficient) |

## Decision Criteria

The basic principle is **Read APIs = Autopilot, Write APIs = HitL (Human-in-the-Loop) Copilot**.

Conditions where Autopilot is appropriate:

- The operation is read-only and irreversible damage does not occur even if it malfunctions
- Eval, canary releases, and audit trails are in place for immediate anomaly detection
- The equivalent operation has been performed repeatedly by humans and the agent's behavior has been sufficiently verified

Conditions where Copilot (HitL) should be maintained:

- Operations include irreversible actions like updates, deletions, or approvals
- Writing to core business systems (ERP, CRM, HR systems)
- The impact of an operation mistake is widespread and rollback is difficult or impossible

Expansion to Autopilot should proceed unhurried and incrementally. The judgment of "making something Autopilot before infrastructure is ready" is the greatest risk.

## Hybrid and Gradual Approach

A practical hybrid uses Copilot/Autopilot differently per operation type even within the same agent.

1. Start all operations in Copilot mode and observe human approval patterns.
2. Identify operations with high approval rates (almost always approved) that are also low-risk.
3. Apply eval and canary to identified operations to narrow down Autopilot candidates.
4. Execute Autopilot conversion with kill switch ([GV-9](../../patterns/gv-governance/gv9-incident-response-kill-switch.md)) and audit trail ([GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)) in place.
5. Re-run eval periodically and revert to Copilot if behavior degrades.

## Related Patterns

- [RT-3 Risk-Tiered Autonomy](../../patterns/rt-runtime/rt3-risk-tiered-autonomy.md)
- [RT-6 SoR Write Boundary](../../patterns/rt-runtime/rt6-sor-write-boundary.md)
- [GV-7 Evaluation Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)
