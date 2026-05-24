---
title: "「相反する仕組み」の選定基準"
description: "OBO vs サービスアカウント、中央レイク vs Mesh、Copilot vs Autopilot など12軸の二者択一の判断基準。"
status: done
---

# 「相反する仕組み」の選定基準

二者択一に見える対立の多くは「どこで線を引くか」が答えである。エンタープライズで決定的な12軸を示す。

## 5.1 OBO委譲 vs サービスアカウント

| 観点 | User OBO（[ID-2](../patterns/id-identity/id2-identity-federation-obo.md)） | Service Account | Agent Identity（[ID-3](../patterns/id-identity/id3-workload-agent-identity.md)） | Hybrid |
|---|---|---|---|---|
| 権限忠実性 | 高 | 低（判定バグ＝漏洩） | 中 | 高 |
| 対応範囲 | 委譲対応SaaSのみ | どのAPIでも | 自律ジョブ | 広い |
| 監査帰責 | 本人に明確 | 曖昧になりがち | エージェントに明確 | 明確 |
| 実装 | 複雑 | 容易 | 中 | 複雑 |

**基準**：個人業務支援＝User OBO。部門代表業務＝Agent Identity＋部門ポリシー。全社バッチ＝Service Account＋厳格監査＋高リスク分類。高リスク操作＝User OBO＋人間承認。最も実務的なのは「**実行主体は Agent、権限上限は User**」の Hybrid である。

## 5.2 中央集権データレイク vs フェデレーテッド Context Mesh

| 観点 | 中央集権ベクトルDB/レイク | Federated Context Mesh（[KM-2](../patterns/km-knowledge/km2-context-mesh.md)） |
|---|---|---|
| 向き | 分析・BI・統計 | 権限付きAI文脈取得 |
| メリット | 高速・集計容易 | 権限を維持しやすい |
| デメリット | 権限のミリ秒同期が事実上不可能→漏洩 | レイテンシ・実装複雑 |

**基準**：権限不要の公開社内規程は中央ベクトル DB へ。機密 SaaS データは本人トークンで JIT 取得するフェデレーテッドへ。**ハイブリッドが必須**。事前索引する場合も ACL 同梱（[KM-1](../patterns/km-knowledge/km1-access-controlled-rag.md)）を必須にする。**「速いから機密も索引化」は禁忌**。

## 5.3 単一エージェント vs RACIマルチエージェント

**基準**：まず単一。マルチ化の基準は「複雑だから」でなく「**企業内の責任分担が複数に分かれるから**」（[RT-2](../patterns/rt-runtime/rt2-raci-multi-agent.md)）。複数部門関与・専門分化・最終責任が重い業務でマルチ、単純 Q&A・低遅延・低コストは単一。マルチはコスト・遅延・複雑性・障害点が増える。

## 5.4 Read-only vs Write-capable（段階的拡張）

**基準**：`Read-only → Draft-only → 承認付き Write → 低リスク自動 Write → 高リスク統制 Write` の順で段階拡張する。参照系は Autopilot、更新系は SoR 経由（[RT-6](../patterns/rt-runtime/rt6-sor-write-boundary.md)）＋ HitL（[RT-4](../patterns/rt-runtime/rt4-human-approval-chain.md)）の Copilot に分離する。

## 5.5 Copilot（業務支援）vs Autopilot（業務代行）

**基準**：経営は Autopilot の ROI を求めるが、確率的挙動による基幹（Workday/SAP/Salesforce）破壊は許容できない。**参照系 API＝Autopilot、更新系 API＝HitL の Copilot** を明確に分離する。Autopilot 化は eval・カナリア・監査が揃った領域から段階的に進める。

## 5.6 個人の記憶 vs プロジェクト/チームの記憶

**基準**：個人効率化は個人メモリ、サイロ化防止は共有メモリが要る。**Personal Enclave（個人領域）と Project Workspace（共有領域）を物理的・論理的に分離**（[KM-4](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) / [RT-11](../patterns/rt-runtime/rt11-project-digital-twin.md)）し、共有範囲を組織グラフに従わせる。一本化は漏洩・混線の温床である。

## 5.7 全プロンプトログ vs 選択的トレースログ

**基準**：再現性のため本文は残したいが、ログ基盤に平文で全件は機密・コストで破綻する。**メタは Trace DB、本文は暗号化ストレージ、集計は DWH** の三層分離（[OB-1](../patterns/ob-observability/ob1-observability-lake.md)）を適用する。極秘処理（[KM-7](../patterns/km-knowledge/km7-ephemeral-secure-context-bus.md)）はメタのみ。

## 5.8 中央集権プラットフォーム vs 部署フェデレーション

**基準**：認可・監査・モデル統制・コスト・憲法・評価は**中央集権**（GV/ID 面）。ドメイン知識・ユースケース・エージェント中身は**各部署にフェデレート**（[GV-3](../patterns/gv-governance/gv3-department-agent-factory.md) のテンプレで権限委譲）。「中央が全部作る」も「各部署が野放し」も失敗する。**中央がガードレールと舗装路を、部署が業務ロジックを**持つ二層統治。

## 5.9 コネクタ自前構築 vs 既存iPaaS再利用

**基準**：既存統合資産がある領域は再利用（[IN-4](../patterns/in-integration/in4-existing-ipaas-reuse.md)）。ただし認可粒度が権限忠実（[ID-4](../patterns/id-identity/id4-permission-mirror-least-of.md)）を満たすか検証する。新規・独自は MCP 化（[IN-1](../patterns/in-integration/in1-tool-mcp-gateway.md)）。

## 5.10 内部/オンプレモデル vs 外部API

**基準**：極秘・規制データ・大量定常→VPC 内/社内推論。一般機密・最新性能・変動需要→外部 API（DPA・リージョン・保持を統制）。[GV-5](../patterns/gv-governance/gv5-central-model-gateway.md) がデータ分類で自動ルーティングする。

## 5.11 同期 vs 非同期

**基準**：数秒で終わる対話は同期＋ストリーミング。10 秒超・多段階・承認待ちは非同期＋永続ワークフロー（[RT-8](../patterns/rt-runtime/rt8-durable-workflow.md)）。部分結果を即ストリーム、重い処理は非同期化のハイブリッドが実用的である。

## 5.12 プロンプトで守る vs ポリシー/実行基盤で守る

**基準**：答えは明確である。**プロンプトはセキュリティ境界にならない**。安全保証は権限・承認・検証・隔離・Policy-as-Code（[ID-7](../patterns/id-identity/id7-policy-as-code-guardrail.md)）で実行基盤側に置く。プロンプトは品質・ふるまいの調整に使う。

!!! danger "プロンプトでの安全保証は禁忌"
    「プロンプトに『機密情報を出力するな』と書けば安全」という設計は、プロンプトインジェクションで容易に突破される。安全保証は必ず実行基盤側（権限・認可・Policy Engine）に置く。
