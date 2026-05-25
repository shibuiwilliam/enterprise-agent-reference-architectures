---
title: "TO-8 Central Platform vs. Department Federation"
description: "Two-layer governance design guidance: authentication, audit, and model control belong to the center; domain knowledge, use cases, and agent content are federated to departments."
status: done
---

# TO-8 Central Platform vs. Department Federation

## Overview

If a central AI CoE tries to build every agent, it cannot keep up with front-line needs — and departments end up launching "rogue agents" on their own. Conversely, if departments are given complete autonomy, security configurations become inconsistent and auditing becomes impossible. Both extremes fail. Two-layer governance — where the center controls authentication, auditing, and cost, while departments own business logic and domain knowledge — is the only practical solution.

## Comparison

| Perspective | Centralized | Department Federation |
|---|---|---|
| Responsibility Area | Authentication/authorization, audit, model control, cost, constitution, evaluation | Domain knowledge, use cases, agent content |
| Primary Patterns | [GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md) / [ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md) | [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) templates |
| Failure Patterns | Center cannot cover all use cases; slow releases | Security configurations vary by department; auditing is impossible |
| Decision Speed | Slow | Fast |
| Safety | High (unified policy) | Low (departmental variation) |

## Decision Criteria

Determine center vs. department based on the nature of the function.

**What the center manages (GV/ID plane)**:

- Authentication/authorization infrastructure (IdP integration, token issuance)
- Audit log and trace collection and storage
- Certification and update management for approved models
- Cost tracking and quota allocation ([GV-8](../../patterns/gv-governance/gv8-cost-quota-chargeback.md))
- Security policy (Policy-as-Code) establishment and enforcement ([ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md))
- Agent evaluation criteria and quality gates ([GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md))

**What is federated to departments (delegated authority via [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md) templates)**:

- Business domain knowledge, FAQs, and rules
- Department-specific use case definitions and prompts
- Agent appearance and channel configuration
- Internal departmental approval flows (within the framework established by the center)

Failure to maintain this division leads to problems. The "center builds everything" model cannot respond quickly enough to departmental needs, gets ignored by front-line staff, and leads to proliferating rogue agents. The "departments run wild" model results in information leakage and compliance violations due to inconsistent security policies.

## Hybrid and Gradual Approach

The correct sequence is to establish the central infrastructure first, then have departments build agents on top of it using templates.

1. Establish the Agent Control Plane with [GV-1](../../patterns/gv-governance/gv1-agent-control-plane.md) to put central authentication, auditing, and cost management in place.
2. Define Policy-as-Code with [ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md) and apply it uniformly to all agents.
3. Provide an Agent Factory template for departments via [GV-3](../../patterns/gv-governance/gv3-department-agent-factory.md), creating an environment where departments can build agents through self-service.
4. Ensure that agents built by departments are automatically incorporated into the central audit and evaluation pipeline.

## Related Patterns

- [GV-1 Agent Control Plane](../../patterns/gv-governance/gv1-agent-control-plane.md)
- [GV-3 Department Agent Factory](../../patterns/gv-governance/gv3-department-agent-factory.md)
- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md)
