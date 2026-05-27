---
title: "KM-6 DLP & Redaction Boundary (DLP & Masking)"
description: "A pattern that applies DLP detection, masking, and tokenization at all input/output boundaries — LLM, RAG, tool execution, and logs — preventing PII, secrets, and contract information from being sent externally or mixing into logs."
status: done
pattern_id: KM-6
facet: knowledge
requires: []
required_by: []
applies_when: [personal_data, external_llm_api, privacy_regulation, confidential_data]
not_applicable_when: [public_data_only, real_time_latency]
risk_tiers: [2, 3, 4, 5]
key_technologies: [Microsoft Purview, Google Cloud DLP / Sensitive Data Protection, "Presidio (Microsoft OSS)", GitGuardian, truffleHog, HashiCorp Vault Transit Secrets Engine, "Format-Preserving Encryption (FPE)", Fluentd / Logstash masking plugins]
---

# KM-6 DLP & Redaction Boundary (DLP & Masking)

## Overview

The confidentiality leak paths of agents are not limited to "LLM input." Unless masking is placed at all five boundaries — LLM output, RAG results, tool execution results, and log storage — gaps remain. This pattern detects PII, secret keys, and contract amounts with DLP and removes them via masking or tokenization. For the most highly classified data, transmission to external LLMs is prohibited entirely, routing to an internal inference infrastructure.

## Enterprise Problem Addressed

Customer personal information and contract information retrieved by RAG being sent to external LLMs, agent output accidentally containing secret keys, detailed debug logs recording personal information in plaintext — these are actual leak paths that can occur in enterprise agents.

The assumption "only checking input is sufficient" is the greatest risk. Documents retrieved by RAG may contain sensitive information from the original documents, and tool execution results (database responses, etc.) carry the same risk. LLM output can expose input sensitive information in transformed form, and prompts and responses sent to log infrastructure for debugging can leave sensitive information in plaintext. A structure placing controls at all five boundaries is necessary.

!!! tip "Minimum Viable Configuration (MVP)"
    Place regex-based PII detection and masking at the two LLM input and output boundaries. Boundaries for tool results and logs are added in the next phase; first dramatically reduce leak risk with the two input/output boundaries.

## Value Hypothesis

Automatic masking of sensitive information prevents the costs of information leak incidents (fines, reputation damage, response effort) before they occur. A safe information usage environment enables expansion of agent application scope.

## Solution and Design

Data passes through five boundaries in order: "Input → DLP/Secret scan → Masking/Tokenization → LLM/Tool → Output DLP → Response/Log." The type and treatment of sensitive information detected at each boundary is recorded as events and sent to [OB-1 Observability Lake](../ob-observability/ob1-observability-lake.md).

```mermaid
flowchart LR
    subgraph Input["Input Boundary"]
        USER[User input / RAG chunk]
        DLP_IN[DLP & secret scan]
        REDACT[Masking / Tokenization]
    end

    subgraph Routing["Routing Decision"]
        CLASS{Data classification}
        INTERNAL["Internal-only path<br/>(Top secret)"]
        EXTERNAL[External LLM path]
    end

    subgraph Exec["Execution Layer"]
        LLM[LLM / Tool execution]
        TOOL_RES[Tool execution results]
    end

    subgraph Output["Output Boundary"]
        DLP_OUT[Output DLP check]
        LOG_FILTER[Log filtering]
        RESP[Response / Log storage]
    end

    USER --> DLP_IN --> REDACT --> CLASS
    CLASS -- Top secret --> INTERNAL --> LLM
    CLASS -- Standard --> EXTERNAL --> LLM
    LLM --> TOOL_RES --> DLP_OUT --> LOG_FILTER --> RESP
```

There are two masking approaches. One is irreversible masking (replacing PII with `[REDACTED]` for storage in logs in a form that cannot be restored). The other is tokenization (replacing PII with a substitute token, stored in a vault for restoration when needed). The latter is for use cases requiring aggregation and search, and restoration requires a separate authorization check.

## When to Use / When Not to Use

| When to Use | When Not to Use |
|---|---|
| All enterprise use cases that may handle PII, sensitive information, or secret keys | Internal tools handling only public information (may become excessive control) |
| Using external LLM APIs (Claude/GPT, etc.) | Fully isolated, internal-only infrastructure where external transmission is physically impossible |
| GDPR/APPI require control evidence for PII processing | Very strict real-time latency processing (DLP scanning may become a bottleneck) |
| Risk of sensitive data mixing into log infrastructure | |

## Component Technologies and System Integration

- **Microsoft Purview**: tenant-wide information protection policy and labeling
- **Google Cloud DLP / Sensitive Data Protection**: API-based PII detection and masking
- **Presidio (Microsoft OSS)**: customizable PII detection and anonymization library
- **Secret scanning**: GitGuardian API / truffleHog secret detection logic integration
- **Tokenization**: HashiCorp Vault Transit Secrets Engine, Format-Preserving Encryption (FPE)
- **Output filtering**: custom regex + ML classifier post-scan of LLM output
- **Log filtering**: masking plugins in log collection pipelines (Fluentd/Logstash)

## Pitfalls and Selection Criteria

!!! danger "Only checking input and missing output and logs"
    "As long as user input is checked, there won't be leaks" is incorrect. RAG-retrieved documents, tool execution results, LLM outputs — each is an independent leak path. Sensitive information is also recorded in plaintext during log storage. Apply controls at all five boundaries.

!!! warning "Service outage from DLP rule over-detection"
    Excessively strict DLP rules mask normal business information and render agents practically unusable. Adjust detection rules by business type and regularly measure false positive rates for tuning.

- If access controls for restoring masked tokens are absent, masking is meaningless. Require a separate authorization check for restoration.
- When DLP scan latency is a problem, choose between async scanning (returning the response first then post-scanning and recording later) and sync scanning (blocking) by use case. However, do not make high-risk operations that require synchronous scanning asynchronous.

## Interfaces

The following are the key interfaces for implementing this pattern. Coding agents can generate stub code from these definitions.

```yaml
interfaces:
  - name: Input DLP Gate
    description: "Scans user input and RAG chunks for PII and secrets before sending to the LLM; applies masking or tokenization and routes highest-classification data to an internal inference path."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Error occurred during Input DLP Gate processing"
    protocol: "REST / gRPC"
    implementation_hints:
      - "See the Solution and Design section for details"
    code_examples:
      typescript: |
        interface InputDlpGateRequest {
          userInput: string;
          ragChunks: string[];
          classification: string;
        }
        interface InputDlpGateResponse {
          sanitizedInput: string;
          maskedTokens: object[];
          routeTo: string;
        }
        interface InputDlpGate {
          inputDlpGate(req: InputDlpGateRequest): Promise<InputDlpGateResponse>;
        }
      python: |
        @dataclass
        class InputDlpGateRequest:
            user_input: str
            rag_chunks: list[str]
            classification: str
        
        @dataclass
        class InputDlpGateResponse:
            sanitized_input: str
            masked_tokens: list[dict]
            route_to: str
        
        class InputDlpGate(Protocol):
            async def input_dlp_gate(self, req: InputDlpGateRequest) -> InputDlpGateResponse: ...
  - name: Output DLP Gate
    description: "Post-scans LLM output and tool results for residual sensitive data before returning to the user or writing to logs."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Error occurred during Output DLP Gate processing"
    protocol: "REST / gRPC"
    implementation_hints:
      - "See the Solution and Design section for details"
    code_examples:
      typescript: |
        interface OutputDlpGateRequest {
          llmOutput: string;
          toolResults: object[];
        }
        interface OutputDlpGateResponse {
          sanitizedOutput: string;
          redactedFields: string[];
        }
        interface OutputDlpGate {
          outputDlpGate(req: OutputDlpGateRequest): Promise<OutputDlpGateResponse>;
        }
      python: |
        @dataclass
        class OutputDlpGateRequest:
            llm_output: str
            tool_results: list[dict]
        
        @dataclass
        class OutputDlpGateResponse:
            sanitized_output: str
            redacted_fields: list[str]
        
        class OutputDlpGate(Protocol):
            async def output_dlp_gate(self, req: OutputDlpGateRequest) -> OutputDlpGateResponse: ...
  - name: Log Filter
    description: "Strips PII from log collection pipeline (Fluentd/Logstash) so that audit logs do not contain plaintext sensitive data."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Error occurred during Log Filter processing"
    protocol: "REST / gRPC"
    implementation_hints:
      - "See the Solution and Design section for details"
    code_examples:
      typescript: |
        interface LogFilterRequest {
          logEntry: object;
          pipelineStage: string;
        }
        interface LogFilterResponse {
          filteredEntry: object;
          strippedFields: string[];
        }
        interface LogFilter {
          logFilter(req: LogFilterRequest): Promise<LogFilterResponse>;
        }
      python: |
        @dataclass
        class LogFilterRequest:
            log_entry: dict
            pipeline_stage: str
        
        @dataclass
        class LogFilterResponse:
            filtered_entry: dict
            stripped_fields: list[str]
        
        class LogFilter(Protocol):
            async def log_filter(self, req: LogFilterRequest) -> LogFilterResponse: ...
```

## Related Patterns

- [GV-5 Central Model Gateway](../gv-governance/gv5-central-model-gateway.md) — Complementary: model gateway integrating input/output filtering
- [KM-7 Ephemeral Secure Context Bus](km7-ephemeral-secure-context-bus.md) — Similar: top-secret processing pattern that volatilizes context itself for even higher confidentiality requirements
- [KM-1 Access-Controlled RAG](km1-access-controlled-rag.md) — Complementary: access control serving as the prerequisite for applying DLP to RAG chunks
- [OB-1 Observability Lake](../ob-observability/ob1-observability-lake.md) — Complementary: observability infrastructure as the destination for DLP event recording
- [ID-1 Workforce/Customer Split](../id-identity/id1-workforce-customer-split.md) — Complementary: setting different confidentiality boundaries per dimension
