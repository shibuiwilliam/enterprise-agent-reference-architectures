---
title: "IN-3 Rate / Quota Broker（レート/クォータ調停）"
description: "1万人規模のユーザーが利用するエージェントのSaaS APIレート上限を、優先度・テナント公平性・バックプレッシャーを備えたトークンバケット型ブローカーで集中管理し、バッチジョブによる全社枯渇を防ぐパターン。"
status: done
pattern_id: IN-3
facet: integration
requires: []
required_by: []
applies_when: [more_than_1000_users_sharing_same_saas_via_agents, batch_jobs_and_interactive_use_coexisting, monthly_saas_api_request_quota_exists]
not_applicable_when: [poc_small_scale_with_ample_api_quota, agents_only_call_internal_apis_with_no_rate_limits, no_rate_limited_saas_in_use]
risk_tiers: [1, 2, 3]
key_technologies: ["Redis (Lua atomic bucket operations)", Envoy Rate Limit Service, Kong Rate Limiting Plugin, Apigee Quota Policy, RabbitMQ Priority Queue, Redis Sorted Set]
---

# IN-3 Rate / Quota Broker（レート/クォータ調停）

## 概要

数万人が同じ Salesforce を使うエンタープライズで、ある部門のバッチ処理が API レート上限を使い切ると、全社員が 429（Too Many Requests）を受ける。このパターンは SaaS ごとにトークンバケットを持ち、対話（優先高）とバッチ（優先低）で公平に枠を配分し、429 発生時は集中リトライで制御する調停レイヤーだ。各エージェントが個別にリトライする設計は SaaS を叩き潰す原因になる。

## 解決する企業課題

エージェントが普及すると「夜間バッチが Salesforce の API 枠を使い切って、翌朝の営業担当が一切エージェントを使えない」という事態が発生する。SaaS API レート枠は企業の業務継続性に直結する共有リソースであり、計画的な配分なしには安定した運用ができない。

個々のエージェントが各自で 429 リトライを実装すると、同期的なリトライストームが発生して SaaS をさらに圧迫する。「バックオフしながら各自でリトライ」という直感的な実装が逆効果になる典型例だ。部門間の公平性が保証されなければ、一部部門の処理が他部門の業務を妨げる組織的な問題に発展する。集中ブローカーによる管理はこれらを構造的に解決する。

!!! tip "最小成立条件（MVP）"
    最もレート制限の厳しい SaaS 1つに対し、Redis ベースのトークンバケットと優先度キュー（interactive > batch の2段）を実装する。テナント公平配分は利用部門が増えてから追加すればよい。

## 価値仮説

API制限の適切な管理により、業務ピーク時のスロットリングによる処理遅延を防ぐ。安定した処理スループットの確保は、SLA遵守とユーザー体験の維持に効く。

## 解決策と設計

全エージェントの SaaS API 呼び出しは Rate Broker を経由する。Broker は SaaS ごとのトークンバケットを管理し、枯渇に近づくとバックプレッシャー（遅延・拒否）を上流に返す。429 を受けた場合は Broker が指数バックオフで集中リトライし、個々のエージェントには再試行させない。

```mermaid
flowchart TB
    subgraph Agents["エージェント群"]
        A1["インタラクティブ<br/>エージェント × N"]
        A2["バッチ<br/>エージェント × M"]
    end

    subgraph Broker["Rate / Quota Broker"]
        PQ["優先度キュー<br/>interactive > batch"]
        TB["トークンバケット<br/>（SaaS ごと）"]
        FAIR[テナント公平配分]
        BP[バックプレッシャー制御]
        RETRY["集中リトライ<br/>指数バックオフ"]
    end

    subgraph SaaS["SaaS APIs"]
        SF[Salesforce]
        SN[ServiceNow]
        OTHER[その他 SaaS]
    end

    A1 -->|優先高| PQ
    A2 -->|優先低| PQ
    PQ --> TB --> FAIR --> BP
    BP -->|通過| SF & SN & OTHER
    SF & SN & OTHER -->|429| RETRY
    RETRY --> TB
    BP -->|満杯・上限近し| A1 & A2
```

トークンバケットの設定は SaaS ごとに行う。バケット容量（バースト許容量）・補充レート（定常上限）・テナント最大シェアを定義する。テナント公平配分は、一テナントが消費できるトークン比率に上限を設ける（例：1テナント最大全体の 30%）。上限接近時はバックプレッシャーとして遅延通知または拒否を上流エージェントに返し、自律的な流量制御を促す。

## 向き／不向き

| 向き | 不向き |
|---|---|
| 1000人以上のユーザーが同一SaaSをエージェント経由で利用する | PoC・小規模（〜数十人）で SaaS API 枠に余裕がある |
| バッチジョブとインタラクティブ利用が混在する | エージェントが内部APIのみを呼び SaaS API 制限がない |
| SaaS API の月間クォータ（リクエスト数上限）がある | レート制限の厳しい SaaS が1つもない |
| 部門間の公平配分を保証したい | |

## 要素技術・既存システム連携

- **トークンバケット実装**：Redis（Lua スクリプトによる原子的バケット操作）、Envoy Rate Limit サービス
- **API Gateway 機能**：Kong Rate Limiting プラグイン、Apigee Quota ポリシー
- **SaaS ごとの API 上限**：Salesforce API Request Limits、ServiceNow Rate Limiting、Slack API Tier
- **集中リトライ**：指数バックオフ + ジッター（thundering herd 防止）
- **優先度キュー**：AMQP 優先キュー（RabbitMQ）、Redis Sorted Set

## 落とし穴／選定の勘所

!!! danger "個々のエージェントが各自で 429 リトライする設計"
    個々のエージェントが 429 を受けて独自にリトライすると、リトライが同期的に集中してリトライストームが発生し SaaS をさらに圧迫する。429 のリトライは必ず Rate Broker に集中させ、エージェント側は Broker からのバックプレッシャー（遅延通知）を受け取るだけにする。

!!! warning "バッチジョブへの同等優先度付与"
    バッチジョブをインタラクティブ利用と同等の優先度にすると、バッチが枠を消費してリアルタイム利用を妨げる。バッチは明示的に低優先度に設定し、閑散時間帯に実行するスケジューリングと組み合わせる。

- SaaS ごとのレート上限はドキュメントと実測の両方で把握する。公称値と実際の制御が異なる SaaS もある。
- Rate Broker 自体が単一障害点になるため、Active-Standby または分散型の可用性設計が必要である。Broker がダウンしても SaaS への直接呼び出しにフォールバックできる仕組みを持つ場合は、そのフォールバック経路も統制する。

## Interfaces

以下はこのパターンを実装する際の主要インターフェイスである。コーディングエージェントはこの定義からスタブコードを生成できる。

```yaml
interfaces:
  - name: Token Bucket per SaaS
    description: "Per-SaaS bucket with configurable burst capacity, refill rate, and per-tenant maximum share; approaching exhaustion triggers back-pressure to upstream agents."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Token Bucket per SaaS の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
  - name: Priority Queue
    description: "Separates interactive (high priority) and batch (low priority) requests; batch is scheduled to off-peak hours when quota is constrained."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Priority Queue の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
  - name: Centralized Retry Handler
    description: "Absorbs 429 responses from SaaS APIs and retries with exponential back-off plus jitter; individual agents receive only back-pressure signals, never raw 429s."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Centralized Retry Handler の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
```

## 関連パターン

- [IN-1 Tool / MCP Gateway](in1-tool-mcp-gateway.md) — 補完：Rate Broker を組み込むツール呼び出し統合入口
- [IN-2 SaaS Connector / Adapter](in2-saas-connector-adapter.md) — 補完：Rate Broker が管理する SaaS 接続層
- [GV-8 Cost / Quota Chargeback](../gv-governance/gv8-cost-quota-chargeback.md) — 補完：テナント別のAPI消費量の課金・チャージバックに Rate Broker の計測データを活用する
- [EX-1 Enterprise Agent Gateway](../ex-experience/ex1-enterprise-agent-gateway.md) — 補完：Rate Broker と連携するレート制御を担うエントリポイント
