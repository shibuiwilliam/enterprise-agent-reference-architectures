---
title: "IN-4 Existing iPaaS Reuse（既存統合資産の再利用）"
description: "エージェントのSaaS統合をゼロから作らず、既存のMuleSoft/Workato/Boomi/社内ESBなどiPaaSを再利用し、新規統合はMCP、既存統合はiPaaSというハイブリッド構成で重複投資と保守分散を防ぐパターン。"
status: done
pattern_id: IN-4
facet: integration
requires: ["IN-1"]
required_by: []
applies_when: [existing_ipaas, cross_saas, enterprise_scale]
not_applicable_when: [poc_phase, single_team]
risk_tiers: [1, 2, 3]
key_technologies: [MuleSoft Anypoint Platform, Workato, Boomi AtomSphere, Apache Camel / IBM MQ, Apigee / Kong, "MCP Adapter (thin wrapper)"]
---

# IN-4 Existing iPaaS Reuse（既存統合資産の再利用）

## 概要

エージェント導入のたびに SaaS 統合をゼロから作り直すのは、既に動いている MuleSoft や Workato のフローを無視した二重投資だ。このパターンは既存の iPaaS 統合フロー・変換ロジック・認証設定をそのまま再利用し、新規に必要な統合だけ MCP で追加するハイブリッド構成を取る。ただし、iPaaS の認可粒度がユーザー単位の権限忠実性を満たすかは事前に検証が必要だ。

## 解決する企業課題

iPaaS で運用中の統合フローは、接続設定・変換ロジック・エラーハンドリング・監視の4つが作り込まれた資産だ。これをエージェント導入のたびに作り直すと、同じ SaaS 接続を2箇所で保守する状態になり、変更・障害対応・セキュリティパッチの適用がすべて二重化してしまう。

統合チームと AI チームが分離している組織では、既存フローの内部知識（SaaS の挙動の癖、変換ロジックの経緯、エラー処理の特殊ケースなど）が統合チームに集中している。ゼロから再実装すると、その知識を再習得するコストが発生する。ハイブリッド再利用はこの重複を排除し、既存チームの保守スキルと運用知識を引き継げる形だ。既存フローのセキュリティ監査済みの実績もそのまま継承できる。

!!! tip "最小成立条件（MVP）"
    既存 iPaaS の最も利用頻度の高いフロー1本を MCP アダプターでラップし、Tool Gateway 経由で呼び出せるようにする。アダプターはインターフェース変換のみとし、ロジックは iPaaS 側に残す。

## 価値仮説

既存iPaaS資産の再利用により、エージェント基盤の構築コストと期間を圧縮する。既存投資を活かした迅速な展開は、価値実現までの時間を短縮する。

## 解決策と設計

エージェントのツール呼び出しは [IN-1 Tool/MCP Gateway](in1-tool-mcp-gateway.md) を経由する。Gateway は新規統合を MCP サーバーとして直接呼ぶ。既存統合については iPaaS の API（または Trigger Webhook）をラップした MCP アダプターを介して呼び出す。既存 iPaaS フローの更新はエージェント側に影響しない。

```mermaid
flowchart TB
    subgraph Agent["エージェント"]
        LLM[LLM / Orchestrator]
    end

    subgraph ToolGW["IN-1 Tool / MCP Gateway"]
        GW[MCP Gateway]
    end

    subgraph NewIntegrations["新規統合（MCP）"]
        MCP1["MCP Server A<br/>新 SaaS 直接統合"]
        MCP2["MCP Server B<br/>新 API 統合"]
    end

    subgraph LegacyAdapter["既存統合ラッパー（MCP Adapter）"]
        WRAP["MCP Adapter<br/>（iPaaS API ラッパー）"]
    end

    subgraph iPaaS["既存 iPaaS"]
        MUL[MuleSoft フロー]
        WRK[Workato レシピ]
        ESB[社内 ESB / Boomi]
    end

    subgraph SaaS["SaaS / オンプレ"]
        SF[Salesforce]
        SN[ServiceNow]
        ERP[ERP / オンプレ]
    end

    LLM --> GW
    GW --> MCP1 & MCP2
    GW --> WRAP --> MUL & WRK & ESB
    MCP1 & MCP2 --> SF & SN
    MUL & WRK & ESB --> SF & SN & ERP
```

既存 iPaaS フローを MCP アダプターでラップする際は、フローの入出力インターフェースのみをエージェント向けに整形し、フロー内部のビジネスロジック・変換・エラーハンドリングは iPaaS 側に残す。アダプターはインターフェース変換のみを担い、ロジックは iPaaS 側に留める——これが二重保守を防ぐ肝心の設計判断だ。

## 向き／不向き

| 向き | 不向き |
|---|---|
| 既に MuleSoft/Workato/Boomi 等が稼働しており統合フローが多数ある | エージェント導入が初めての統合であり iPaaS 自体がない |
| 統合チームと AI チームが分離しており既存フローの引き継ぎが困難 | 既存フローの品質が低く再利用より作り直しが合理的な場合 |
| 段階的移行（既存フローは残しつつエージェント対応を追加）が必要 | SaaS 接続が数件しかなく MCP 直接実装の工数が少ない |

## 要素技術・既存システム連携

- **MuleSoft Anypoint Platform**：フローをAPIとして公開し MCP アダプターから呼び出す
- **Workato**：Webhook トリガーまたは API レシピで外部呼び出しを受け付ける
- **Boomi AtomSphere**：プロセスをAPI エンドポイントとして公開
- **社内 ESB（IBM MQ / Apache Camel等）**：既存のサービスインターフェース仕様を維持してラップ
- **Apigee / Kong**：既存 iPaaS の前段に配置された API Management をそのまま活用
- **MCP Adapter**：iPaaS の API を MCP ツール仕様に変換する薄いラッパー

## 落とし穴／選定の勘所

!!! warning "iPaaS の認可粒度が粗く権限忠実性（ID-4）が崩れる"
    既存 iPaaS フローが「全権サービスアカウント」で動いている場合、エージェントがそのフローを呼ぶと意図せず広いアクセスを行うことになる。既存フローを採用する前に、フローが使う認証情報のスコープを確認し、[ID-4 Permission Mirror & Least-of](../id-identity/id4-permission-mirror-least-of.md) の原則との整合を検証する。

!!! warning "iPaaS のスロットリングがエージェントに透過しない"
    既存 iPaaS フローは人間向けの呼び出し頻度を前提に設計されているケースが多い。エージェントによる高頻度呼び出しでフロー側のレート制限や同時実行制限に当たることがある。[IN-3 Rate/Quota Broker](in3-rate-quota-broker.md) で呼び出し頻度を制御する。

- MCP アダプターにビジネスロジックを書き込むと、結局 iPaaS と二重保守になる。アダプターはインターフェース変換のみを担い、ロジックは iPaaS 側に留めること。
- 既存フローの変更（iPaaS 側）がエージェントの動作に影響することがある。MCP アダプターに契約テスト（Consumer-Driven Contract Test）を設け、フロー変更時の回帰検証を自動化する。

## Interfaces

以下はこのパターンを実装する際の主要インターフェイスである。コーディングエージェントはこの定義からスタブコードを生成できる。

```yaml
interfaces:
  - name: MCP Adapter (iPaaS Wrapper)
    description: "Thin translation layer that converts MCP tool-call format to the iPaaS API or webhook trigger; all business logic remains inside the iPaaS flow."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "MCP Adapter (iPaaS Wrapper) の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface McpAdapterRequest {
          mcpToolCall: object;
          iPaasEndpoint: string;
          authToken: string;
        }
        interface McpAdapterResponse {
          iPaasResult: object;
          translatedResponse: object;
        }
        interface McpAdapter {
          mcpAdapter(req: McpAdapterRequest): Promise<McpAdapterResponse>;
        }
      python: |
        @dataclass
        class McpAdapterRequest:
            mcp_tool_call: dict
            i_paas_endpoint: str
            auth_token: str
        
        @dataclass
        class McpAdapterResponse:
            i_paas_result: dict
            translated_response: dict
        
        class McpAdapter(Protocol):
            async def mcp_adapter(self, req: McpAdapterRequest) -> McpAdapterResponse: ...
  - name: iPaaS Flow (existing)
    description: "Existing integration flow with its connection config, transformation logic, error handling, and monitoring retained as-is."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "iPaaS Flow (existing) の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface IpaasFlowRequest {
          flowId: string;
          inputPayload: object;
          triggerSource: string;
        }
        interface IpaasFlowResponse {
          outputPayload: object;
          executionId: string;
          status: string;
        }
        interface IpaasFlow {
          ipaasFlow(req: IpaasFlowRequest): Promise<IpaasFlowResponse>;
        }
      python: |
        @dataclass
        class IpaasFlowRequest:
            flow_id: str
            input_payload: dict
            trigger_source: str
        
        @dataclass
        class IpaasFlowResponse:
            output_payload: dict
            execution_id: str
            status: str
        
        class IpaasFlow(Protocol):
            async def ipaas_flow(self, req: IpaasFlowRequest) -> IpaasFlowResponse: ...
  - name: Contract Test Suite
    description: "Consumer-driven contract tests on the MCP adapter to auto-detect when iPaaS flow changes break the agent-facing interface."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Contract Test Suite の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface ContractTestSuiteRequest {
          adapterId: string;
          contractVersion: string;
          testScenarios: string[];
        }
        interface ContractTestSuiteResponse {
          passed: boolean;
          failures: string[];
          testedAt: Date;
        }
        interface ContractTestSuite {
          contractTestSuite(req: ContractTestSuiteRequest): Promise<ContractTestSuiteResponse>;
        }
      python: |
        @dataclass
        class ContractTestSuiteRequest:
            adapter_id: str
            contract_version: str
            test_scenarios: list[str]
        
        @dataclass
        class ContractTestSuiteResponse:
            passed: bool
            failures: list[str]
            tested_at: datetime
        
        class ContractTestSuite(Protocol):
            async def contract_test_suite(self, req: ContractTestSuiteRequest) -> ContractTestSuiteResponse: ...
```

## 関連パターン

- [IN-1 Tool / MCP Gateway](in1-tool-mcp-gateway.md) — 補完：iPaaS アダプターを含む全ツール呼び出しの統合入口
- [IN-2 SaaS Connector / Adapter](in2-saas-connector-adapter.md) — 対比：新規 SaaS 接続における MCP 直接実装との使い分け
- [ID-4 Permission Mirror & Least-of](../id-identity/id4-permission-mirror-least-of.md) — 補完：iPaaS 経由時の権限忠実性の確認と最小権限の適用
- [ID-2 Identity Federation & OBO](../id-identity/id2-identity-federation-obo.md) — 補完：iPaaS フロー経由でも本人権限を伝播するための委譲設計
