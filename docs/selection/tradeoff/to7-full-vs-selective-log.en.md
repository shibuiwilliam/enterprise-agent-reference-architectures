---
title: "TO-7 Full Prompt Log vs. Selective Trace Log"
description: "Design guidance for balancing cost, confidentiality, and reproducibility through three-layer separation: meta in Trace DB, body in encrypted storage, and aggregate in DWH."
status: done
---

# TO-7 Full Prompt Log vs. Selective Trace Log

## Overview

When an incident occurs, "what was input and what was returned at that time" must be reproducible — otherwise root cause investigation hits a dead end. But piping all prompts in plain text into the logging infrastructure spreads customers' personal information and confidential data across log storage, itself becoming a security incident seed. This covers how to design a practical middle ground — three-layer separation — between "wanting to record everything" and "not wanting to spread confidential data."

## Comparison

| Log Type | Storage | Contains | Purpose |
|---|---|---|---|
| Trace Metadata | Trace DB ([OB-1](../../patterns/ob-observability/ob1-observability-lake.md)) | Request ID, model, latency, tool call names, error codes | Monitoring, alerting, cost tracking |
| Prompt Body | Encrypted storage ([DC-3](../degree/dc3-log-granularity.md)) | Actual prompt and response text | Reproduction, debugging, audit |
| Aggregate / Analytics | DWH | Anonymized and aggregated token counts, quality metrics, etc. | Improvement, reporting |

## Decision Criteria

Three-layer separation ([DC-3](../degree/dc3-log-granularity.md) / [OB-1](../../patterns/ob-observability/ob1-observability-lake.md)) is the standard configuration.

Decision axes for log design:

- **Reproducibility**: Store the minimum information needed for bug investigation or audit in body storage. Target not all records, but error occurrences, high-risk operations, and random samples.
- **Confidentiality**: Encrypt body storage and limit access to incident responders and security teams. Plain text storage in metadata DB is prohibited.
- **Cost**: Storing all prompt body records with high token counts causes storage costs to skyrocket. Design filtering rules for storage targets at the design stage.

Handling special cases:

- **Top-secret processing ([KM-7](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md))**: Do not store the body; store only metadata (request ID, timestamp, processing completion flag). Prioritize proving "the fact of execution" over content reproducibility.
- **Regulated data**: Set retention periods and deletion rules in accordance with GDPR, personal information protection laws, etc. Prioritize regulatory compliance over reproducibility.

!!! warning "Plain Text Full Prompt Storage — Forbidden"
    Storing prompts containing confidential information in plain text in a general logging infrastructure is a cause of security incidents. Body storage is limited to encrypted storage; access rights must be minimized.

## Hybrid and Gradual Approach

Start operations with a minimal configuration that stores metadata only, and add body storage in the range where necessity has been confirmed.

1. Build monitoring and alerting with trace metadata ([OB-1](../../patterns/ob-observability/ob1-observability-lake.md)) only.
2. Add body storage in encrypted storage when the need for debugging or audit arises.
3. Establish selection rules for storage targets (on error, on high-risk operations, N% sampling).
4. Add a DWH aggregation layer to run quality improvement loops with anonymized data.

## Related Patterns

- [OB-1 Enterprise Agent Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md)
- [KM-7 Ephemeral Secure Context Bus](../../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)
- [DC-3 Log Granularity](../degree/dc3-log-granularity.md)
