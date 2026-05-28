---
title: "TO-12 Guard with Prompts vs. Policy/Execution Platform"
description: "Prompts do not constitute security boundaries. The principle that safety guarantees must be placed on the execution platform side — through permissions, approvals, verification, isolation, and Policy-as-Code."
status: done
---

# TO-12 Guard with Prompts vs. Policy/Execution Platform

## Overview

Is writing "do not output confidential information" in a system prompt sufficient for security? The answer is clearly "no." A prompt that can be bypassed simply by entering "ignore the above instructions" does not constitute a security boundary. Safety guarantees must be placed on the execution platform side — in permissions, authorization, and Policy Engines — while prompts are used for adjusting response tone and output format. This role separation is a core principle of enterprise design.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-12
decision_rules:
  - condition: "control_type IN ['access_control', 'approval_flow', 'output_validation', 'sandbox_isolation']"
    recommendation: prompt_for_quality_platform_for_security
    reason: "Access control, approval flows, DLP output validation, and execution sandboxing must be enforced by the platform, not prompts"
  - condition: "control_type IN ['output_format', 'response_style', 'task_context', 'language_setting']"
    recommendation: prompt_for_quality_platform_for_security
    reason: "Output format, tone, task context, and language specification are appropriate for prompt engineering; not security boundaries"
  - condition: "security_enforced_by_prompt == true"
    recommendation: platform_only
    reason: "Anti-pattern: prompt-only security is bypassed by prompt injection ('ignore above instructions...'); never use prompts as security boundary"
  - condition: "infrastructure_readiness == 'incomplete' AND security_enforced_by_prompt == true"
    recommendation: platform_only
    reason: "First establish platform access control (ID-4) and Policy-as-Code (ID-7); no prompt is a valid substitute for missing infrastructure"
  - condition: "defense_in_depth == true"
    recommendation: prompt_for_quality_platform_for_security
    reason: "Layered defense: platform handles security enforcement, prompts handle behavior quality; both used together at appropriate layers"
```

## Comparison

| Perspective | Guard with Prompts | Policy/Execution Platform ([ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)) |
|---|---|---|
| Security Effectiveness | Invalid (bypassable via prompt injection) | Valid (permissions and Policy Engine judge at execution platform level) |
| Suitable For | Quality control, output format, behavior adjustment | Access control, approval flow, data protection |
| Ease of Bypass | High (easily circumvented with malicious input) | Low (controlled at code level) |
| Auditability | Low (difficult to verify prompt intent after the fact) | High (change history preserved as Policy-as-Code) |
| Maintenance | Non-systematic, person-dependent | Systematically managed as Policy-as-Code |

## Decision Criteria

The answer to this question is not a binary choice, but a clear division of roles.

**What the execution platform (policy, permissions, approval) must handle**:

- Access control: who can access which data and tools is determined by the permissions system ([ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md) / [ID-6](../../patterns/id-identity/id6-zero-trust-pdp-pep.md))
- Approval flow: insert human approval before executing high-risk operations ([RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md))
- Output verification: inspect generated text for confidential data via DLP ([RT-5](../../patterns/rt-runtime/rt5-command-envelope.md))
- Execution environment isolation: limit the range of operations an agent can perform via sandboxing
- Policy-as-Code: define prohibited and required operations as code, automatically applied by the agent runtime ([ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md))

**What prompts should handle (quality and behavior adjustment)**:

- Specifying output format (bullet points, JSON, tables, etc.)
- Adjusting response style (polite, concise, professional, etc.)
- Providing task purpose and background information
- Specifying language and terminology

!!! danger "Using Prompts for Security Guarantees is Prohibited"
    A design that relies on "writing constraints in prompts" can be easily circumvented by prompt injection attacks. A design where constraints are removed simply by an attacker entering "ignore the above instructions..." holds no value as a security measure. Safety guarantees must always be placed on the execution platform side (permissions, authorization, Policy Engine).

## Hybrid and Gradual Approach

Prompt control and execution platform control are not mutually exclusive — they are combined as defense-in-depth, each playing an appropriate role.

Implementation priority:

1. First establish execution platform-side access control ([ID-4](../../patterns/id-identity/id4-permission-mirror-least-of.md)) and Policy-as-Code ([ID-7](../../patterns/id-identity/id7-policy-as-code-guardrail.md)). Without these, no amount of prompt refinement can guarantee security.
2. Add approval flow ([RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)) and output verification/DLP ([RT-5](../../patterns/rt-runtime/rt5-command-envelope.md)).
3. Complete the structure where all requests are authorized through PDP/PEP ([ID-6](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)).
4. Only after execution platform controls are in place, perform prompt engineering for quality improvement and behavior adjustment.

## Related Patterns

- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md)
- [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md)
- [RT-5 Command Envelope](../../patterns/rt-runtime/rt5-command-envelope.md)
