---
title: "RT-4 Human Approval Chain（組織解決型承認）"
description: "エージェントが提案した操作を組織図から動的に解決した承認者が審査し、委譲・エスカレーション・SLA 管理を伴う既存ワークフローツールで承認チェーンを完結させるパターン。"
status: done
pattern_id: RT-4
facet: runtime
requires: ["RT-8", "ID-7"]
required_by: []
applies_when: [high_risk_ops, hitl_approval, org_chart_maintained, write_operations]
not_applicable_when: [real_time_latency, poc_phase]
risk_tiers: [3, 4]
key_technologies: [Temporal, AWS Step Functions, Workday HCM, Microsoft Entra, Slack Block Kit, ServiceNow, OpenTelemetry]
---

# RT-4 Human Approval Chain（組織解決型承認）

## 概要

エージェントは「この契約を更新しますか？」と提案するまでが仕事だ。実行は人間の承認後に始まる。このパターンでは、組織グラフ（Workday の組織図）から上長・所管責任者・コスト所有者を動的に解決して承認を求める。承認者をコードに直書きすると異動で宛先不明になるため、常に組織グラフから都度解決する設計が欠かせない。Slack や ServiceNow での承認体験、不在時の代理委譲、SLA タイマー、却下理由のフィードバックまでをセットで設計する。

## 解決する企業課題

不可逆操作（大量メール送信・資金移動・権限変更）をエージェントが直接実行すると、誤判断時の損害が大きい。承認チェーンは実行前の人間介在を構造として保証し、エージェントの自律度を「提案まで」に限定する仕組みだ。

「誰が承認者か」が属人的知識に依存している企業では、担当者の異動・休暇時に承認フローが止まる。承認者がハードコードされていると、組織変更のたびに設定変更が必要になり、変更漏れが積み重なる。組織図からの動的解決はこの問題を構造的に排除し、常に適切な権限を持つ承認者を特定できるようにする。

監査の観点でも重要な役割がある。承認行為の記録（誰がいつどの理由で承認・否決したか）は内部統制・規制対応に不可欠だ。否決理由は同種リクエストの再提案品質を改善するフィードバックシグナルにもなる。

!!! tip "最小成立条件（MVP）"
    Slack ボタンによる単一承認者フロー。組織図 API から承認者を1名解決し、承認 or 否決の結果をログに記録する最小構成。委譲・エスカレーション・SLA タイマーは後続フェーズで追加する。

## 価値仮説

承認の自動ルーティングにより、承認待ち時間（リードタイム）を短縮する。人間の判断が必要な操作に安全にエージェントを適用でき、高リスク業務の自動化範囲を拡大する。

## 解決策と設計

解決策の核心は2点だ。第一に、承認者を静的定義でなく組織図から動的に解決すること。第二に、承認体験を既存ツールに埋め込むこと。従業員が新規システムを学習する手間をなくし、採用の障壁を下げる。

承認フローは4つのフェーズで構成される。

1. **承認者解決**：リクエストの種類・対象リソース・コスト・リスク Tier（RT-3）を入力として、組織図から適切な承認者（ライン管理職、コストオーナー、データオーナー）を動的に特定する。
2. **承認依頼送信**：既存ワークフローツールへ通知を送信し、承認者がアクションできる UI（Slack ボタン、ServiceNow タスク等）を提供する。
3. **SLA 監視・エスカレーション**：承認期限を設定し、タイムアウト時は上位承認者へ自動エスカレーションする。
4. **結果記録**：承認・否決・委譲の理由と判断者をデシジョンログに記録し、否決理由はエージェントの学習フィードバックに渡す。

```mermaid
sequenceDiagram
    participant AGT as Agent
    participant AE as Approval Engine
    participant ORG as 組織図 (Workday/Entra)
    participant TOOL as ワークフローツール<br/>(Slack/ServiceNow)
    participant APPR as 承認者
    participant AUDIT as 監査ログ

    AGT->>AE: 操作提案 + リスク Tier
    AE->>ORG: 承認者解決クエリ
    ORG-->>AE: 承認者リスト
    AE->>TOOL: 承認依頼送信
    TOOL->>APPR: 通知（ボタン付き）
    alt 承認
        APPR->>TOOL: 承認
        TOOL->>AE: 承認済み
        AE->>AGT: 実行許可
    else 否決
        APPR->>TOOL: 否決 + 理由
        TOOL->>AE: 否決
        AE->>AGT: 否決 + 理由（学習フィードバック）
    else タイムアウト
        AE->>ORG: 上位承認者解決
        AE->>TOOL: エスカレーション通知
    end
    AE->>AUDIT: 判断記録
```

承認者の解決ロジックは組織構造の変化（異動・昇格・退職）に追従させる必要がある。ハードコードは組織変更のたびに障害を引き起こしかねない。組織図 API をリアルタイムで参照して承認者を動的に導出する設計が望ましい。

## 向き／不向き

| 向き | 不向き |
|---|---|
| 不可逆性・高リスクの操作（資金移動、権限付与、顧客連絡）を含む業務フロー | レイテンシ要件が厳しく、人間介在を許容できないリアルタイム処理 |
| 組織図が整備されており、承認者を役職・コスト権限・データオーナーシップで特定できる企業 | 承認フローが過剰になり業務効率を著しく損なう低リスク操作（Tier 0〜1） |
| 既存の承認ワークフローツール（ServiceNow、Slack ワークフロー、Workday）が導入済みの環境 | 組織図が整備されておらず、承認者解決の基盤がない段階 |

## 要素技術・既存システム連携

- 承認エンジン：カスタム実装、または Temporal ワークフロー、AWS Step Functions
- 組織図・権限情報：Workday HCM、Microsoft Entra（旧 Azure AD）、BambooHR
- 権限委譲管理：委譲期間・範囲の記録と自動失効
- SLA タイマー：エスカレーション自動化
- ワークフローツール統合：Slack（Block Kit ボタン）、ServiceNow（タスク自動生成）、Workday 承認フロー
- デジタル署名：高リスク承認の非否認性確保
- 監査ログ：承認者・理由・タイムスタンプの構造化記録（OpenTelemetry）

## 落とし穴／選定の勘所

**承認者のハードコード**。「このリクエストは山田部長が承認する」とコードに直接記述すると、組織変更のたびに設定変更が必要になり変更漏れが生じる。承認者は常に組織図から動的に解決し、退職・異動後も正しい承認者にルーティングされる設計を維持すること。

**エスカレーション設計の欠如**。SLA を設定しても上位承認者への自動エスカレーションがなければ、承認がサイレントに滞留する。エスカレーション先の定義と通知経路は必ず設計に含めること。

**否決理由の捨て置き**。否決理由は、エージェントが同種のリクエストを適切に修正するための最も価値ある学習シグナルだ。理由を監査ログに埋めるだけでなく、エージェントの提案生成に反映するフィードバックループを構築したい。

**委譲の無制限連鎖**。承認者が別の承認者に委譲し、さらに委譲される連鎖は責任の所在を不透明にする。委譲は1ホップに制限し、委譲先の資格要件を組織図から検証すること。

## Interfaces

以下はこのパターンを実装する際の主要インターフェイスである。コーディングエージェントはこの定義からスタブコードを生成できる。

```yaml
interfaces:
  - name: Approver Resolution Engine
    description: "Queries the org chart API to dynamically identify the correct approver (line manager, cost owner, data owner) per request type and risk tier."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Approver Resolution Engine の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface ApproverResolutionEngineRequest {
          requestType: string;
          riskTier: number;
          requesterId: string;
          resourceId: string;
        }
        interface ApproverResolutionEngineResponse {
          approverId: string;
          approverRole: string;
          escalationChain: string[];
        }
        interface ApproverResolutionEngine {
          approverResolutionEngine(req: ApproverResolutionEngineRequest): Promise<ApproverResolutionEngineResponse>;
        }
      python: |
        @dataclass
        class ApproverResolutionEngineRequest:
            request_type: str
            risk_tier: int
            requester_id: str
            resource_id: str
        
        @dataclass
        class ApproverResolutionEngineResponse:
            approver_id: str
            approver_role: str
            escalation_chain: list[str]
        
        class ApproverResolutionEngine(Protocol):
            async def approver_resolution_engine(self, req: ApproverResolutionEngineRequest) -> ApproverResolutionEngineResponse: ...
  - name: Workflow Tool Notification
    description: "Sends approval requests with action buttons to Slack or ServiceNow tasks so approvers can act within familiar tools."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Workflow Tool Notification の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface WorkflowToolNotificationRequest {
          approverId: string;
          approvalRequestId: string;
          operationSummary: string;
          actionButtons: string[];
        }
        interface WorkflowToolNotificationResponse {
          notificationId: string;
          deliveredAt: Date;
          channel: string;
        }
        interface WorkflowToolNotification {
          workflowToolNotification(req: WorkflowToolNotificationRequest): Promise<WorkflowToolNotificationResponse>;
        }
      python: |
        @dataclass
        class WorkflowToolNotificationRequest:
            approver_id: str
            approval_request_id: str
            operation_summary: str
            action_buttons: list[str]
        
        @dataclass
        class WorkflowToolNotificationResponse:
            notification_id: str
            delivered_at: datetime
            channel: str
        
        class WorkflowToolNotification(Protocol):
            async def workflow_tool_notification(self, req: WorkflowToolNotificationRequest) -> WorkflowToolNotificationResponse: ...
  - name: Decision Log
    description: "Records the approver identity, decision (approve/deny/delegate), reason, and timestamp for internal control evidence."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Decision Log の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
    code_examples:
      typescript: |
        interface DecisionLogRequest {
          projectId: string;
          decisionText: string;
          alternatives: string[];
          rationale: string;
          authorId: string;
        }
        interface DecisionLogResponse {
          decisionId: string;
          recordedAt: Date;
        }
        interface DecisionLog {
          decisionLog(req: DecisionLogRequest): Promise<DecisionLogResponse>;
        }
      python: |
        @dataclass
        class DecisionLogRequest:
            project_id: str
            decision_text: str
            alternatives: list[str]
            rationale: str
            author_id: str
        
        @dataclass
        class DecisionLogResponse:
            decision_id: str
            recorded_at: datetime
        
        class DecisionLog(Protocol):
            async def decision_log(self, req: DecisionLogRequest) -> DecisionLogResponse: ...
```

## 関連パターン

- [RT-3 Risk-Tiered Autonomy](rt3-risk-tiered-autonomy.md)：補完関係。Tier 3〜4 の操作に対して本パターンの承認フローを起動する。Tier 判定がトリガーとなる。
- [RT-5 Intent-to-Enterprise Command Envelope](rt5-command-envelope.md)：補完関係。Command Envelope の `requires_approval` フラグが true の場合に本パターンの承認チェーンを起動する。
- [RT-7 Enterprise Saga](rt7-enterprise-saga.md)：補完関係。補償不可能な Saga ステップ（顧客メール送信など）の手前に承認チェーンを挟む。
- [ID-7 Policy-as-Code Guardrail](../id-identity/id7-policy-as-code-guardrail.md)：補完関係。承認が必要かどうかの判定をポリシーとして実装し、実行基盤側で強制する。
- [OB-2 Unified Audit & Lineage](../ob-observability/ob2-unified-audit-lineage.md)：補完関係。承認者・理由・タイムスタンプを監査ログに記録し、内部統制の証跡を確保する。
