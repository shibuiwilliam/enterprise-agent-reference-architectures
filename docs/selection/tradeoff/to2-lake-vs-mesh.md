---
title: "TO-2 中央集権データレイク vs フェデレーテッド Context Mesh"
description: "知識基盤を中央集権ベクトルDBで構築するかフェデレーテッドContext Meshで構築するかの判断基準。"
status: done
---

# TO-2 中央集権データレイク vs フェデレーテッド Context Mesh

## 概要

社内の全文書を中央のベクトル DB に索引化すれば検索は速い。しかし Salesforce の商談レコードのように閲覧権限が人によって異なるデータまで索引化すると、権限変更の反映が追いつかず「見えてはいけないデータが見える」事故が起きる。中央集権レイクとフェデレーテッド Context Mesh（[KM-2](../../patterns/km-knowledge/km2-context-mesh.md)）のどちらを選ぶか——実際には「公開情報はレイク、機密は Mesh」というハイブリッドが必須だ。その線引きをどこで引くかが設計の核心になる。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-2
decision_rules:
  - condition: "data_sensitivity == 'public' AND permission_change_frequency == 'low'"
    recommendation: central_lake
    reason: "権限不要の公開情報（社内規程・公開ナレッジベース）は中央ベクトルDBへ索引化し、高速に取得できる"
  - condition: "data_sensitivity == 'confidential' OR data_type == 'personal_saas_records'"
    recommendation: federated_mesh
    reason: "機密SaaSデータ（個人のSalesforceレコード等）は本人トークンでJIT取得するフェデレーテッドMeshへ。権限の同期問題を回避する"
  - condition: "pre_indexed == true AND acl_required == true"
    recommendation: central_lake
    reason: "事前索引する場合もACL同梱（KM-1）を必須にすれば中央レイクを使ってよい"
  - condition: "data_sensitivity == 'public' AND confidential_data_in_result == true"
    recommendation: hybrid
    reason: "公開情報はレイクで高速に、機密情報はMeshで権限を維持して取得し、KM-3で統合ルーティングする"
```

## 比較

| 観点 | 中央集権ベクトル DB／レイク | Federated Context Mesh（[KM-2](../../patterns/km-knowledge/km2-context-mesh.md)） |
|---|---|---|
| 向き | 分析・BI・統計 | 権限付き AI 文脈取得 |
| メリット | 高速・集計容易 | 権限を維持しやすい |
| デメリット | 権限のミリ秒同期が事実上不可能 → 漏洩 | レイテンシ・実装複雑 |

## 判断基準

- **権限不要の公開情報**（社内規程・公開ナレッジベース）→ 中央ベクトル DB へ索引化。高速に取得できる
- **機密 SaaS データ**（個人の Salesforce レコード・Workday 情報等）→ 本人トークンで JIT 取得するフェデレーテッド Mesh へ。権限の同期問題を回避できる
- **事前索引する場合**も ACL 同梱（[KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md)）を必須にする

!!! danger "「速いから機密も索引化」は禁忌"
    中央ベクトル DB に機密データを索引化すると、権限変更の反映遅延が漏洩に直結する。速度のために機密データの権限保証を犠牲にしてはならない。

## ハイブリッド・段階的アプローチ

ハイブリッドが必須だ。公開情報はレイクで高速に取得し、機密情報は Mesh で権限を維持して取得する。両者を [KM-3 Knowledge Graph](../../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) で統合的にルーティングする構成が、実務的な落としどころになる。

## 関連パターン

- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — ACL 同梱での事前索引
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — フェデレーテッド取得の設計本体
- [KM-3 Canonical Object & Knowledge Graph](../../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) — 統合ルーティング
- [ID-2 Identity Federation & OBO](../../patterns/id-identity/id2-identity-federation-obo.md) — 本人トークンでの JIT 取得
