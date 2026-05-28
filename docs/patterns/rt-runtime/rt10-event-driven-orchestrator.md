---
title: "RT-10 Event-Driven Enterprise Orchestrator（イベント駆動）"
description: "人間からの呼び出しを待たず、SaaSや社内システムのイベントをトリガーにエージェントを自律起動し、複数システムにまたがる処理をバックエンドで完結させるパターン。"
status: done
pattern_id: RT-10
facet: runtime
requires: ["RT-7", "RT-8"]
required_by: []
applies_when: [event_driven, async_processing, cross_saas, autonomous_exec]
not_applicable_when: [real_time_latency, single_team]
risk_tiers: [2, 3, 4]
key_technologies: [Amazon EventBridge, Google Pub/Sub, Azure Service Bus, Apache Kafka, CloudEvents, Debezium, Temporal, Workato, MuleSoft]
decision_keys: [TO-11, DC-9]
value_drivers: [automation, revenue_growth]
kpis: ["イベント処理レイテンシ", "自動対応率"]
maturity_stage: execution
mvp: "1イベントソース（Webhook）からのトリガーで自動処理を構築"
cost_orientation: M
---

# RT-10 Event-Driven Enterprise Orchestrator（イベント駆動）

## 概要

「入社が完了しました」というイベントが Workday から飛んだ瞬間に、エージェントが自律起動して IDP アカウント作成・ライセンス付与・Slack チャンネル招待・Jira ボード初期設定・歓迎メール送信をまとめて実行する——これがイベント駆動エージェントの姿です。人間が呼び出すのを待たず、業務プロセスの進行がエージェントを自然に起動します。RPA では扱えない例外や判断の揺らぎを LLM が吸収し、書き込み操作には非同期 Saga と人間承認を組み合わせます。バックオフィス自動化において、エージェントの経営価値が最も直接的に発揮される構成です。

## 解決する企業課題

このパターンは従来のシステム連携における受動性の問題を解決します。エージェントを「呼ばれたときだけ動く」存在ではなく、業務プロセスの流れに沿って自律的に動くバックエンドワーカーとして機能させます。人間のオペレーターが介在しなければ進まなかった業務フローを常時自律稼働させることで、バックオフィスの抜本的な自動化が実現できます。

Workday・Salesforce・GitHub など複数 SaaS の間で発生するコピー&ペースト作業（オンボーディング時のアカウント作成、契約更新時の通知連携、コードマージ後のドキュメント更新など）は、コストが高くミスも起きやすいシステム間連携の典型例です。RPA は HTML 構造変化に脆く例外パターンへの対処が難しいですが、エージェントは自然言語理解によって非定型の例外を処理できます。

Webhook が増加するにつれ「誰がどの Webhook をどう処理しているか」が管理不能になります（Webhook 混乱）。イベントバスを中心とした一元管理で Webhook の散在を解消し、イベントの認証・フィルタリング・デバウンス・コスト管理をゲートウェイ層に集約することで、安全なイベント駆動基盤を構築できます。

!!! tip "最小成立条件（MVP）"
    1つの SaaS イベント（例：Workday の onboarding_completed）をイベントバス経由で受信し、2〜3ステップの Durable Workflow を起動する構成。デバウンスと HMAC 署名検証をゲートウェイ層に入れれば最小成立です。

## 価値仮説

イベント駆動による自律的な業務起動は、人間の「次の作業を始める」判断と手動入力を不要にします。端到端の業務自動化を実現し、処理リードタイムの大幅短縮とコスト削減に効きます。

## 解決策と設計

解決策の核心は「SaaS のイベントをエンタープライズのビジネスイベントとして標準化し、エージェントをそのコンシューマとして設計すること」です。イベントバスをシステム間の疎結合な接続点とし、エージェントはイベントの意味を解釈して適切なアクションを選択します。書き込みを伴う処理は Saga パターンで実行し、リスク判定に基づいて HitL 承認を挟みます。

イベントバスを介して SaaS からイベントを受け取り、オーケストレーターがワークフローを起動します。

```mermaid
sequenceDiagram
    participant WD as Workday
    participant EB as イベントバス
    participant GW as Agent Gateway
    participant OR as Orchestrator
    participant IDP as IdP（Okta）
    participant SL as Slack
    participant AP as 承認者（HitL）

    WD->>EB: onboarding_completed イベント
    EB->>GW: Webhook受信・認証検証
    GW->>OR: ワークフロー起動（冪等性キー付き）

    OR->>IDP: アカウント作成API
    IDP-->>OR: 完了

    OR->>SL: チャンネル招待API
    SL-->>OR: 完了

    OR->>AP: 高リスク操作：権限付与の承認依頼（Slack）
    AP-->>OR: 承認

    OR->>IDP: 権限グループ追加API
    IDP-->>OR: 完了

    OR->>SL: 完了通知 → 担当者
```

トリガー条件・レートリミット・デバウンス・リスク分類は、オーケストレーター起動前のゲートウェイ層で評価します。同一イベントが短時間に複数発火した場合（イベントストーム）はデバウンスで重複起動を防ぎます。ワークフロー実行中の予算上限・ステップ上限は Durable Workflow エンジン（RT-8）に委譲する形です。

外部 Webhook は HMAC 署名検証・送信元 IP ホワイトリスト・CloudEvents の `source` フィールド検証で認証します。不正なイベントを起動前に遮断し、Webhook 偽装攻撃を防ぐ設計にしてください。

## 向き／不向き

| 向き | 不向き |
|---|---|
| SaaSが発する標準的なイベント（オンボーディング完了、契約更新、インシデント検知など）を起点とする業務フローが存在する | ユーザーが即座に応答を必要とするインタラクティブな処理（同期チャット、リアルタイム検索など） |
| 複数システムにまたがるコピー&ペースト作業や定型連携を自動化したい | イベント発火頻度が極端に高く（毎秒数百件以上）、エージェント起動コストが非現実的な処理 |
| 処理の大部分が非同期・バックグラウンドで完結し、人間がリアルタイムで待機する必要がない業務 | トリガー条件が定義できないほどアドホックな業務 |
| RPAで自動化を試みたが例外処理の複雑さで断念した経緯がある | — |

## 要素技術・既存システム連携

- **イベントバス**：Amazon EventBridge、Google Pub/Sub、Azure Service Bus、Apache Kafka
- **イベント標準**：CloudEvents（イベント形式の標準化。発信元・種別・IDを統一スキーマで表現）
- **CDC（Change Data Capture）**：Debezium（DBの変更をイベントとして取り出す）
- **ワークフローエンジン**：Temporal、AWS Step Functions、Azure Durable Functions（RT-8と連携）
- **iPaaS**：Workato、MuleSoft、Zapier Enterprise（SaaSとイベントバスの接続・変換）
- **SaaSイベントソース**：Workday（HR）、Salesforce（CRM）、GitHub（開発）、PagerDuty（インシデント）
- **HitL承認チャネル**：Slack（承認ボタン）、ServiceNow（承認タスク）
- **ガバナンス連携**：GV-9 Kill Switchと組み合わせ、暴走時にイベント処理を停止する

## 落とし穴／選定の勘所

!!! danger "イベントストームによるコスト・実行暴走"
    イベントドリブン設計の最大のリスクはイベントストームです。SaaSの一括更新・バッチ処理・障害復旧時などに同一種類のイベントが短時間に大量発火し、エージェントが大量並列起動します。トークン消費・API課金・SaaSレートリミット超過が連鎖的に発生します。対策として以下を必ず設計に組み込んでください：
    1. デバウンス（同一エンティティへの短時間内重複イベントを1件に集約）
    2. レートリミット（ワークフロー起動数の上限）
    3. リスク分類（高コスト処理は自動起動せず承認キューに積む）
    4. 予算上限（月次・日次のトークン・API消費上限とGV-9による緊急停止）

!!! warning "トリガー条件の設計不足"
    「Salesforceの更新イベント」を無条件にトリガーとすると、商談ステータスの微細な変更（営業担当者のメモ追加など）のたびにエージェントが起動します。トリガー条件はフィールド・ステータス・変化量・発信元IPなどで絞り込み、不要な起動を排除してください。

!!! warning "書き込み操作をHitLなしで自動実行しないこと"
    イベント駆動の自律性は魅力的ですが、本番システムへの書き込み（アカウント作成・権限付与・外部送信）を承認なしで全自動化すると、誤イベント・悪意あるイベント注入のリスクが高まります。RT-6のSoR書き込み境界を参照し、高リスク操作はSlack/ServiceNowのHitL承認フローを必ず挟んでください。

!!! warning "イベントの認証・検証省略"
    外部WebhookをそのままエージェントのトリガーとするとWebhook偽装攻撃のリスクがあります。受信時にHMAC署名検証・送信元IPホワイトリスト・CloudEventsの`source`フィールド検証を実施し、不正なイベントを起動前に遮断してください。

## Interfaces

以下はこのパターンを実装する際の主要インターフェイスです。コーディングエージェントはこの定義からスタブコードを生成できます。

```yaml
interfaces:
  - name: Event Gateway
    description: "Validates incoming webhooks via HMAC signature, source IP allowlist, and CloudEvents source field before routing to the orchestrator."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Event Gateway の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface EventGatewayRequest {
          webhookPayload: object;
          hmacSignature: string;
          sourceIp: string;
          cloudEventsSource: string;
        }
        interface EventGatewayResponse {
          validated: boolean;
          routedTo: string;
          eventId: string;
        }
        interface EventGateway {
          eventGateway(req: EventGatewayRequest): Promise<EventGatewayResponse>;
        }
      python: |
        @dataclass
        class EventGatewayRequest:
            webhook_payload: dict
            hmac_signature: str
            source_ip: str
            cloud_events_source: str
        
        @dataclass
        class EventGatewayResponse:
            validated: bool
            routed_to: str
            event_id: str
        
        class EventGateway(Protocol):
            async def event_gateway(self, req: EventGatewayRequest) -> EventGatewayResponse: ...
  - name: Debounce / Rate Limiter
    description: "Collapses duplicate events for the same entity within a short window and enforces a maximum concurrent workflow launch rate."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Debounce / Rate Limiter の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface DebounceRateLimiterRequest {
          entityId: string;
          eventType: string;
          windowMs: number;
          maxConcurrent: number;
        }
        interface DebounceRateLimiterResponse {
          deduplicated: boolean;
          throttled: boolean;
          allowedToProcess: boolean;
        }
        interface DebounceRateLimiter {
          debounceRateLimiter(req: DebounceRateLimiterRequest): Promise<DebounceRateLimiterResponse>;
        }
      python: |
        @dataclass
        class DebounceRateLimiterRequest:
            entity_id: str
            event_type: str
            window_ms: int
            max_concurrent: int
        
        @dataclass
        class DebounceRateLimiterResponse:
            deduplicated: bool
            throttled: bool
            allowed_to_process: bool
        
        class DebounceRateLimiter(Protocol):
            async def debounce_rate_limiter(self, req: DebounceRateLimiterRequest) -> DebounceRateLimiterResponse: ...
  - name: Durable Workflow Engine (RT-8)
    description: "Manages long-running post-event processing with crash resilience and HitL approval integration."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Durable Workflow Engine (RT-8) の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface DurableWorkflowEngineRequest {
          workflowId: string;
          eventPayload: object;
          approvalRequired: boolean;
        }
        interface DurableWorkflowEngineResponse {
          executionId: string;
          state: string;
          startedAt: Date;
        }
        interface DurableWorkflowEngine {
          durableWorkflowEngine(req: DurableWorkflowEngineRequest): Promise<DurableWorkflowEngineResponse>;
        }
      python: |
        @dataclass
        class DurableWorkflowEngineRequest:
            workflow_id: str
            event_payload: dict
            approval_required: bool
        
        @dataclass
        class DurableWorkflowEngineResponse:
            execution_id: str
            state: str
            started_at: datetime
        
        class DurableWorkflowEngine(Protocol):
            async def durable_workflow_engine(self, req: DurableWorkflowEngineRequest) -> DurableWorkflowEngineResponse: ...
```

## 関連パターン

- [RT-7 Enterprise Saga Agent](rt7-enterprise-saga.md)：補完関係。イベントをトリガーとして起動するSagaワークフローの実装に組み合わせ、マルチシステム書き込みの整合性を確保します。
- [RT-8 Durable Enterprise Agent Workflow](rt8-durable-workflow.md)：補完関係。イベント起動後の長時間処理をDurable Workflowとして管理し、クラッシュ耐性と状態永続化を提供します。
- [RT-4 Human Approval Chain](rt4-human-approval-chain.md)：補完関係。書き込み操作前のHitL承認をイベント駆動フローに組み込み、高リスク操作の人間介在を保証します。
- [IN-1 Tool & MCP Gateway](../in-integration/in1-tool-mcp-gateway.md)：補完関係。エージェントから各SaaSへの呼び出しをゲートウェイ経由で管理し、レートリミットと監査を一元化します。
- [GV-9 Incident Response & Kill Switch](../gv-governance/gv9-incident-response-kill-switch.md)：補完関係。イベントストームや暴走時にエージェント実行を緊急停止します。イベント駆動では特に重要な安全装置となります。

## Decision Summary

```yaml
decision_summary:
  pattern: RT-10
  participates_in:
    - decision: TO-11
      role: option_b
    - decision: DC-9
      role: enabler
  recommended_if:
    - "ビジネスイベントに反応して自動アクションを実行したい"
    - "リアルタイム性が求められる"
  avoid_if:
    - "定時バッチで十分"
  combines_with: [RT-7, RT-8, RT-9, IN-1]
  conflicts_with: []
  value_outcome:
    drivers: [automation, revenue_growth]
    kpis: [イベント処理レイテンシ, 自動対応率]
  mvp: "1イベントソースからのトリガーで自動処理を構築"
  cost: M
```
