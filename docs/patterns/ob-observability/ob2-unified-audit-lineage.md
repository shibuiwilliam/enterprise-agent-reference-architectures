---
title: "OB-2 Unified Audit & Lineage（三者帰責）"
description: "すべてのエージェント行為を人＋エージェント＋対象システムの三者で改ざん不能に記録し、完全再構成・規制報告を可能にするパターン。"
status: done
---

# OB-2 Unified Audit & Lineage（三者帰責）

## 概要

エージェントのすべての行為を「人（principal）＋エージェント（workload）＋対象システム（tool/system）」の三者で改ざん不能に記録し、後から誰の依頼で・どのエージェントが・どのシステムに・何をしたかを完全再構成できる統一監査基盤である。OpenTelemetry の Trace ID を相関 ID としてエージェント内の監査と各 SaaS（Salesforce Shield・Google Workspace Audit・Okta System Log）の監査ログを一本化し、インシデント時のリプレイと規制当局への報告を可能にする。

## 解決する企業課題

従来のシステムでは「誰が操作したか（人間の ID）」が監査の基本単位だった。エージェントが介在すると、操作者はエージェントであり、その背後に人間がいるという二層構造になる。「エージェントが Salesforce を更新した」という記録だけでは、それが誰の依頼によるものか、どの権限に基づくものかが不明になる。

金融・医療・製造など規制対象業界では、インシデント時に「誰が・何を・なぜ・どの権限で・いつ」実行したかを規制当局に説明できなければならない。エージェント行為が人間の直接操作と混在してログに残ると、後から分離して追跡することが困難になる。エージェント内の監査と各 SaaS の監査が分断されると、横断的な調査が不可能になる。三者帰責（human + agent + system）という記録フォーマットと、相関 ID による横断追跡が、この課題を構造的に解決する。

## 解決策と設計

各アクションに以下の情報を記録する。

| 記録項目 | 説明 |
|---|---|
| principal | 依頼者（人間のID） |
| workload | エージェント（ワークロードID） |
| tool/system | 対象システム・ツール |
| 入出力ハッシュ | 入力・出力のハッシュ（改ざん検知） |
| ポリシー判断 | allow/deny/require_approval の理由 |
| 委譲チェーン | user → agent → tool の委譲経路 |
| コスト | トークン・API呼び出しコスト |

```mermaid
flowchart TB
    subgraph Action["エージェント行為"]
        A[ユーザー依頼] --> B[エージェント処理]
        B --> C[ツール/SaaS呼び出し]
    end

    subgraph Audit["統一監査ログ"]
        P[principal<br/>人間ID]
        W[workload<br/>エージェントID]
        T[tool/system<br/>対象システム]
        H[入出力ハッシュ]
        POL[ポリシー判断]
        DEL[委譲チェーン]
    end

    subgraph Correlation["横断追跡"]
        CID[相関ID]
        SAAS[各SaaS監査ログ]
        SOR[SoR変更ログ]
    end

    Action --> Audit
    CID --> SAAS
    CID --> SOR
    Audit --> CID
```

相関 ID（OpenTelemetry の Trace ID / Span ID を流用）でエージェント内監査と各 SaaS 監査を貫き、SoR（System of Record）の変更と突合可能にする。委譲チェーン（user → agent → tool）の記録により、「このツール呼び出しは誰の依頼から始まったか」を確実に追跡できる。入出力ハッシュで改ざんを検知し、監査の整合性を保証する。インシデント時はリプレイ（[GV-9](../gv-governance/gv9-incident-response-kill-switch.md)）で過去実行を再現し原因を特定する。

## 向き／不向き

| 向き | 不向き |
|---|---|
| 本番 AI 全般に必須 | — |
| 規制対応が求められる業界 | 不向きなケースは基本的にない |

## 要素技術・既存システム連携

- **SIEM**：Splunk、Microsoft Sentinel
- **SaaS 監査ログ**：Salesforce Shield、Google Workspace Audit、Okta System Log
- **相関 ID**：OpenTelemetry Trace ID / Span ID
- **イベントストア**：Event Store、改ざん不能ログ
- **リプレイ**：[GV-9](../gv-governance/gv9-incident-response-kill-switch.md) のリプレイ機能と連携

## 落とし穴／選定の勘所

!!! warning "エージェントとSaaSの監査分断"
    エージェント側の監査と各 SaaS の監査が分断され横断追跡できないのが最大の落とし穴である。相関 ID で一本化し、SoR の変更と突合可能にする。「エージェント側のログには記録があるが SaaS 側には残っていない」または逆の状況は、調査を致命的に困難にする。

- 監査ログは改ざん不能なストレージに保管する（append-only、WORM）。エージェントやアプリケーション層から監査ログを書き換えられないよう、書き込み専用の権限設計にする。
- 人間の直接操作とエージェント経由の操作を同一フォーマットで記録し、横断検索を可能にする。フォーマットが分かれると SIEM での相関分析が複雑になる。
- ログの保持期間は規制要件に合わせる（金融：7年、医療：10年等）。エージェントの利用が本格化する前に保持ポリシーを確定しておく。

## 関連パターン

- [OB-1 Observability Lake](ob1-observability-lake.md) — 補完：観測データ（トレース・コスト・品質）を監査証跡の素材として活用する
- [GV-9 Incident Response & Kill Switch](../gv-governance/gv9-incident-response-kill-switch.md) — 補完：インシデント時のリプレイ・調査を支える
- [ID-2 Identity Federation & OBO](../id-identity/id2-identity-federation-obo.md) — 補完：委譲チェーン（user → agent → tool）の記録と OBO トークンの追跡
- [ID-6 Zero-Trust PDP/PEP](../id-identity/id6-zero-trust-pdp-pep.md) — 補完：ポリシー判断（allow/deny/require_approval）の記録源
- [RT-6 SoR Write Boundary](../rt-runtime/rt6-sor-write-boundary.md) — 補完：SoR 変更との突合による書き込み操作の完全追跡
