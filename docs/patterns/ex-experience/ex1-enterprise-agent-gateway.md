---
title: "EX-1 Enterprise Agent Gateway（統一フロントドア）"
description: "すべてのエージェント要求が通る単一の入口で、認証・分類・リスク判定・レート制御・監査エントリを一元適用するパターン。"
status: done
---

# EX-1 Enterprise Agent Gateway（統一フロントドア）

## 概要

従業員が Slack からエージェントに話しかけても、Web ポータルから使っても、Salesforce の画面内で呼び出しても、すべてのリクエストが通る「たった1つの入口」を置く。この入口で本人確認・リスク判定・流量制御・監査ログの記録をまとめて済ませるため、チャネルが増えてもセキュリティと統制の品質が下がらない。数万人が一斉に使う朝のピーク時のバースト吸収も、このゲートウェイが引き受ける。

## 解決する企業課題

エンタープライズ AI が複数チャネル（Slack/Web/SaaS 埋め込み/API）から呼ばれるようになると、入口が分散し統制・監査・容量管理が崩れる。チャネルごとに認証方式が異なると権限チェックの網羅性が保証できず、監査ログが分断して事後調査に支障をきたす。数万人規模のバースト（業務時間帯の全社一斉利用）を個々のエージェントが吸収しようとすると、バックエンドに過負荷がかかる。さらに、チャネルごとに個別の統制ロジックを実装すると保守コストが乗数的に増大し、ガバナンスの穴が生じやすい。単一入口を置くことで、これらの問題を構造的に一括して封じる。

## 解決策と設計

Gateway を「実行面への唯一の通路」として位置づけ、すべての統制をここで一括実施する。個別エージェントは認証・リスク判定・監査エントリを持たず、Gateway が保証した本人 ID と相関 ID を受け取るだけでよい。新しいエージェントやチャネルが追加されても統制ロジックを再実装する必要がなくなる。

チャネル（Slack/Web/SaaS埋め込み）を吸収し、本人 ID と相関 ID を後段へ伝播する。Gateway は統制点であり、認証・分類・リスク判定・レート制御・監査を実行する最初の PEP（[ID-6](../id-identity/id6-zero-trust-pdp-pep.md)）でもある。

```mermaid
flowchart TB
    subgraph Channels["チャネル"]
        SL[Slack]
        WEB[Web]
        SF[Salesforce 埋め込み]
        API[API]
    end

    subgraph GW["Enterprise Agent Gateway"]
        AUTH[認証<br/>OIDC/SAML]
        CLS[要求分類<br/>意図判定]
        RISK[リスク分類]
        RATE[レート制御<br/>バースト吸収]
        AUD[監査エントリ<br/>相関ID付与]
    end

    subgraph Backend["実行面"]
        RT[Runtime / Orchestrator]
    end

    Channels --> AUTH
    AUTH --> CLS --> RISK --> RATE --> AUD
    AUD -->|本人ID＋相関ID| RT
```

## 向き／不向き

| 向き | 不向き |
|---|---|
| 複数チャネル・大規模な全社展開 | 単一 PoC で1チャネルのみ |
| 統制・監査要件がある環境 | 完全閉域の実験環境 |
| 従業員/顧客チャネルの分離が必要 | チャネルが1つだけの小規模利用 |
| — | 決定論的な RPA やフォーム処理で完結する定型業務（AI エージェント化自体が不要） |

## 要素技術・既存システム連携

- **API Gateway**：Kong、Apigee、AWS API Gateway
- **認証**：OIDC、SAML 2.0
- **リスク分類**：Risk Scoring、意図分類器
- **相関 ID**：OpenTelemetry Trace ID
- **レート制御**：Token Bucket、バースト吸収

## 落とし穴／選定の勘所

!!! warning "素通しプロキシ化"
    Gateway を素通しプロキシにして認可・監査を後段任せにするのは最大の落とし穴。入口は統制点であり、ここで認証・リスク分類・監査エントリを確実に実行する。

- 従業員チャネルと顧客チャネルは [ID-1 二面分離](../id-identity/id1-workforce-customer-split.md) に従い、信頼境界で分ける。
- Token Exchange（[ID-2 OBO](../id-identity/id2-identity-federation-obo.md)）は Gateway で実行し、後段には OBO トークンを渡す。
- レート制御は [IN-3 Rate/Quota Broker](../in-integration/in3-rate-quota-broker.md) と連携し、SaaS 側のレート上限も考慮する。

## 関連パターン

- [EX-2 業務埋め込み vs 独立ポータル](ex2-embedded-vs-portal.md) — 補完：Gateway 配下のUI提供形態を決定するパターン
- [EX-3 チャネル非依存フロントドア](ex3-channel-agnostic-frontdoor.md) — 補完：Gateway に到達する前のチャネル差吸収を担う
- [ID-1 Workforce/Customer 二面分離](../id-identity/id1-workforce-customer-split.md) — 補完：入口での信頼境界を分離する前提条件
- [ID-2 Identity Federation & OBO](../id-identity/id2-identity-federation-obo.md) — 補完：Gateway での Token Exchange の実装
- [ID-6 Zero-Trust PDP/PEP](../id-identity/id6-zero-trust-pdp-pep.md) — 類似：Gateway が最初の PEP として機能する
- [OB-1 Observability Lake](../ob-observability/ob1-observability-lake.md) — 補完：監査エントリの送信先
