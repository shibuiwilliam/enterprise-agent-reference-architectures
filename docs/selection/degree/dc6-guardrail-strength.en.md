---
title: "DC-6 Guardrail Strength (False Positives vs. False Negatives)"
description: "A continuous parameter for adjusting guardrail thresholds to balance false positive and false negative rates."
status: done
---

# DC-6 Guardrail Strength (False Positives vs. False Negatives)

## Overview

If guardrails are too strict, even legitimate emails get blocked every time on suspicion of "possible confidential leakage," and users stop using the agent. Too lenient and truly dangerous outputs pass through unchecked. This balance cannot be determined uniformly — "external email sending" and "summarizing an internal memo" obviously differ. This covers how to adjust the thresholds of [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) per the risk characteristics of each pathway.

## Harms of Too Little or Too Much

| Extreme | State | Harm |
|---|---|---|
| Too little (too permissive) | Low threshold, many dangerous operations pass through | Serious incidents occur such as confidential information leakage, unauthorized operations, external publication |
| Too much (too strict) | High threshold, most operations blocked by false positives | Legitimate tasks are continuously blocked, halting user work. Creates incentive for "approval fatigue" and "disabling guardrails" |

## Decision Criteria

The basic policy is to separate thresholds by the risk characteristics of each pathway.

- **High-risk pathways** (external transmission, sensitive data access, operations with side effects, customer-facing output): Set strict thresholds and bring FN (false negatives / missed detections) close to zero
- **Low-risk pathways** (read-only, internal drafts, pre-approved templates): Lightweight guardrails are sufficient; minimize FP (false positives / incorrect blocks) that impede operations
- Base threshold settings on "business tolerance." Measure FP and FN rates separately and use which harm is greater in business terms as the decision criterion
- For paths where latency is critical, mitigate impact by selecting async or sampling-based inspection rather than synchronous blocking

Combining with authorization decisions by [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md) makes it easier to record the reason for guardrail-denied operations in audit trails.

!!! warning "Avoid Uniform Threshold Settings"
    Applying the same threshold to all pathways inevitably skews to one extreme or the other. Evaluate risk per pathway and set thresholds individually.

## Adjustment Mechanism

- Periodically measure FP rate, FN rate, and incident count with [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) and use as input for threshold adjustment
- Record guardrail trigger count, type, and pathway in [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) to identify pathways with many false positives
- Link with output filtering in [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) to align content inspection granularity
- Subject threshold changes to change management and compare FP/FN trends before and after changes

## Related Patterns

- [ID-7 Policy-as-Code Guardrail](../../patterns/id-identity/id7-policy-as-code-guardrail.md) — the core guardrail implementation
- [ID-6 Zero-Trust PDP/PEP](../../patterns/id-identity/id6-zero-trust-pdp-pep.md) — integration with authorization decisions
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — FP/FN rate measurement and adjustment
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — alignment with output filtering
