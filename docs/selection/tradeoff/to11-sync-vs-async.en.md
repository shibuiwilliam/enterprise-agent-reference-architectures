---
title: "TO-11 Synchronous vs. Asynchronous"
description: "Design guidance for selecting the processing method based on processing time and the presence of approval flows, combining partial result streaming with asynchronous processing for heavy tasks."
status: done
---

# TO-11 Synchronous vs. Asynchronous

## Overview

"Tell me today's schedule" should return in 2 seconds, but "analyze all contracts from the past 3 years" can take a few minutes. For business processes that require supervisor approval in between, users cannot be expected to keep their browser open waiting for approval. This covers how to distinguish between synchronous, asynchronous, and hybrid approaches based on processing time and the presence of approval steps.

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-11
decision_rules:
  - condition: "expected_duration_seconds <= 5 AND human_approval_step == false AND operation_type == 'qa_or_search'"
    recommendation: synchronous
    reason: "Simple Q&A, search, and document summarization that complete in seconds are suitable for synchronous processing"
  - condition: "expected_duration_seconds > 10 OR steps_include_human_approval == true OR external_api_calls_multiple == true"
    recommendation: asynchronous
    reason: "Processing exceeding 10 seconds, multi-step workflows with human approvals, or multiple sequential/parallel API calls require durable async workflow"
  - condition: "multi_system_transaction == true AND compensation_on_failure_required == true"
    recommendation: saga_transactional
    reason: "Cross-system operations requiring transactional consistency and rollback compensation on partial failure need Saga pattern"
  - condition: "duration_5s_to_30s == true AND ux_responsiveness_important == true"
    recommendation: streaming_sync
    reason: "Stream LLM generation token-by-token; users read as they wait, improving perceived responsiveness for 5-30 second tasks"
  - condition: "sync_started_but_exceeded_timeout == true"
    recommendation: hybrid_timeout_escalation
    reason: "Auto-escalate from sync to async when processing exceeds expected time; deliver completion via webhook or email notification"
```

## Comparison

| Perspective | Synchronous Processing | Asynchronous Processing ([RT-8](../../patterns/rt-runtime/rt8-durable-workflow.md)) |
|---|---|---|
| User Experience | Receives results in real time | Checks results via notification or polling after completion |
| Suitable For | Dialogues, searches, Q&A that complete in seconds | Processes taking 10+ seconds, multi-step processing, approval-pending tasks |
| Fault Tolerance | Processing is lost on network disconnection | State is preserved in persistent storage; resumable |
| Scalability | Maintaining connections is a bottleneck | Easy to parallelize through queues |
| Implementation Complexity | Simple | State management and notification mechanisms required |

## Decision Criteria

Select synchronous, asynchronous, or hybrid based on the characteristics of the processing.

**Conditions where synchronous processing is appropriate**:

- Processing completes within a few seconds
- The user needs results immediately and can wait
- Simple Q&A, search, document summarization, etc.

**Conditions requiring asynchronous processing ([RT-8](../../patterns/rt-runtime/rt8-durable-workflow.md))**:

- Processing exceeds 10 seconds or has indeterminate duration
- Includes multi-step processing (information gathering → analysis → approval → execution)
- Has human approval-pending ([RT-4](../../patterns/rt-runtime/rt4-human-approval-chain.md)) steps
- Calls multiple external APIs sequentially or in parallel
- Processing must continue and be resumable even if a network disconnection occurs

**Conditions requiring the Saga pattern ([RT-7](../../patterns/rt-runtime/rt7-enterprise-saga.md))**:

- Transaction consistency is required for operations spanning multiple systems
- Compensating processing (rollback) is required in case of mid-process failure

## Hybrid and Gradual Approach

A practical hybrid streams partial results immediately and offloads heavy processing to asynchronous mode.

- **Streaming synchronous**: Deliver LLM generation results in a token-by-token stream. Users experience "reading while waiting" rather than just "waiting." Effective for processing lasting seconds to about 30 seconds.
- **Partial completion notifications**: Notify users of intermediate states in asynchronous tasks ("information collection complete," "awaiting approval") in real time, allowing users to track progress.
- **Timeout escalation**: When synchronous processing exceeds the expected time, automatically switch to asynchronous mode and send a completion notification via Webhook or email.

Incremental introduction sequence:

1. First implement basic functionality with synchronous processing.
2. Identify processing that frequently times out and designate it for asynchronous handling.
3. Introduce persistent workflows via [RT-8](../../patterns/rt-runtime/rt8-durable-workflow.md) to safely handle approval-pending steps.
4. Add streaming delivery ([EX-1](../../patterns/ex-experience/ex1-enterprise-agent-gateway.md)) to improve UX for long-running processes.

## Related Patterns

- [RT-8 Durable Workflow](../../patterns/rt-runtime/rt8-durable-workflow.md)
- [RT-7 Enterprise Saga](../../patterns/rt-runtime/rt7-enterprise-saga.md)
- [EX-1 Enterprise Agent Gateway](../../patterns/ex-experience/ex1-enterprise-agent-gateway.md)
