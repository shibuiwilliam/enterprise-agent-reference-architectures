---
title: "KM-1 Access-Controlled Enterprise RAG（権限認識RAG）"
description: "検索/RAGの結果をデータ源のアクセス制御を保ったまま依頼者が見てよいものだけに絞るパターン。"
status: done
pattern_id: KM-1
facet: knowledge
requires: ["ID-2", "ID-4"]
required_by: []
applies_when: [cross_saas_document_ticket_crm_chat_search, frequent_access_changes_from_departures_or_transfers, multiple_saas_integrated_search_required]
not_applicable_when: [data_sources_where_acl_cannot_be_controlled, real_time_db_master_requiring_direct_query, public_information_only_no_acl_needed]
risk_tiers: [1, 2, 3]
key_technologies: ["Hybrid Search (BM25 + Vector)", Reranker, Pinecone, Weaviate, Qdrant, Elasticsearch, Freshness Ranking, Citation]
---

# KM-1 Access-Controlled Enterprise RAG（権限認識RAG）

## 概要

全社文書をベクトル DB に入れて「何でも検索できる AI」を作ると、本来そのユーザーには見えないはずの文書まで回答に含まれてしまう。インデックスにコピーした瞬間に元のアクセス権限が消える——これが企業 RAG 最大の落とし穴だ。このパターンは取り込み時に各チャンクへソースの ACL・分類・鮮度を同梱し、検索のたびに依頼者の最新権限で再評価する。退職者・異動者に「見えてはいけないものが見える」問題を根本から防ぐ。

## 解決する企業課題

エンタープライズ RAG の根本的な危険は、ドキュメントをベクトル DB にコピーした時点で元のアクセス制御が失われることだ。SharePoint の閲覧権限、Box のフォルダ権限、Confluence のスペース制限——これらはインデックス作成時に考慮されなければ意味をなさない。退職者・異動者が以前の職責に関わる文書を参照し続ける問題も、この「ACL 剥奪が伝播しない」構造から生じる。

古い文書への参照（鮮度問題）、根拠不明の回答（引用なし）、複数 SaaS 横断での権限不一致——これらはすべて「コピー先で権限と鮮度を管理していない」ことに起因する。企業の情報ガバナンスは、検索インフラがアクセス制御を忠実に継承することを前提として成立するものだ。

!!! tip "最小成立条件（MVP）"
    単一データ源（例：SharePoint）のチャンクに ACL メタデータを付与し、検索時にユーザーの所属グループで pre-filter する構成。鮮度やリランクは後回しでよいが、ACL 同梱と検索時フィルタの2点は初日から必須である。

## 価値仮説

権限を維持した社内知識検索により、従業員の情報探索時間を大幅に削減する。必要な知識への即時アクセスは意思決定速度と業務品質の向上に直結する。

## 解決策と設計

取り込み時にソースの ACL・分類・鮮度をチャンクに同梱し、検索時点の最新エンタイトルメントで評価する。ACL はキャッシュではなく都度判定を基本とし、権限剥奪をリアルタイムに反映させる。

```mermaid
flowchart LR
    subgraph Ingest["取り込み"]
        SRC[データ源<br/>Box/Drive/Notion/Confluence]
        EMB[Embedding＋ACL同梱<br/>分類・鮮度メタ]
        VDB[(Vector DB)]
    end

    subgraph Query["検索"]
        Q[クエリ]
        CTX[ユーザー/エージェント/<br/>プロジェクト文脈]
        PF[Permission Filter<br/>ID-4 参照]
        HYB[ハイブリッド検索<br/>BM25＋ベクトル]
        RR[リランク]
        ANS[引用付き回答]
    end

    SRC --> EMB --> VDB
    Q --> CTX --> PF
    PF --> HYB --> RR --> ANS
    VDB --> HYB
```

Permission Filter は [ID-4 Permission Mirror](../id-identity/id4-permission-mirror-least-of.md) と連携し、依頼者のエンタイトルメントを検索時に評価する。ハイブリッド検索（BM25＋ベクトル）でキーワード適合と意味的類似を組み合わせ、リランカーが最終スコアを算出する。回答には出典 Citation を必ず含め、根拠の透明性を確保する。鮮度ランキングにより古いドキュメントの優先度を自動的に下げる。

## 向き／不向き

| 向き | 不向き |
|---|---|
| 文書/チケット/CRM/チャットの横断検索 | 権限制御不能なデータ源 |
| 多数の SaaS からの統合検索 | リアルタイム DB 正本（直接クエリすべき） |
| 退職・異動に伴う権限変更が頻繁 | 全社員が見てよい公開情報のみ（ACL 不要） |

## 要素技術・既存システム連携

- **検索**：Hybrid Search（BM25＋ベクトル）、Reranker
- **Vector DB**：Pinecone、Weaviate、Qdrant、Elasticsearch
- **ACL フィルタ**：[ID-4 Permission Mirror](../id-identity/id4-permission-mirror-least-of.md) と連携
- **引用**：Citation 付き回答（根拠の透明化）
- **鮮度**：Freshness Ranking（古い文書の優先度低下）
- **対象 SaaS**：Box、Google Drive、Notion、Confluence、SharePoint

## 落とし穴／選定の勘所

!!! danger "ACL の取り込み時固定"
    ACL を取り込み時に固定し再同期しないのは最も危険なアンチパターンである。退職者・異動者が見続ける問題が発生する。取り込み時の ACL は参考値とし、検索時に最新エンタイトルメントで再評価することを必須とする。

- 「全社データを1つのベクトル DB に入れて速く検索」は禁忌である。ACL 同梱を必須とし、同梱できないデータはフェデレーション（[KM-2](km2-context-mesh.md)）で JIT 取得する。
- 検索結果の引用（Citation）を必ず含め、根拠の透明性を確保する。引用なしの回答は「なぜその答えになったか」の追跡を不可能にする。
- 鮮度ランキングにより古い文書の優先度を下げ、陳腐化した情報による誤回答を防ぐ。特に組織改編・制度変更後は鮮度フィルタが重要になる。

## Interfaces

以下はこのパターンを実装する際の主要インターフェイスである。コーディングエージェントはこの定義からスタブコードを生成できる。

```yaml
interfaces:
  - name: Ingest Pipeline with ACL Embedding
    description: "Embeds source ACL, classification label, and freshness timestamp into each chunk at ingestion time; ACL is treated as a reference value for refresh not a fixed copy."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Ingest Pipeline with ACL Embedding の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
  - name: Permission Filter (ID-4)
    description: "Evaluates the requester's current entitlements against chunk ACLs at query time, filtering inaccessible documents before ranking."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Permission Filter (ID-4) の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
  - name: Hybrid Search + Reranker
    description: "Combines BM25 keyword matching with vector similarity; reranker produces final scored results including freshness penalty for stale documents."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Hybrid Search + Reranker の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
```

## 関連パターン

- [ID-4 Permission Mirror & Least-of](../id-identity/id4-permission-mirror-least-of.md) — 補完：検索時のアクセス制御判定を担う権限評価層
- [KM-2 Context Mesh](km2-context-mesh.md) — 補完：ACL 同梱が困難なデータ源のフェデレーション型 JIT 取得
- [KM-5 Purpose-Bound Context](km5-purpose-bound-context.md) — 補完：検索結果を業務目的に限定してさらに絞り込む
- [KM-6 DLP & Redaction Boundary](km6-dlp-redaction-boundary.md) — 補完：検索結果に含まれる機密情報のマスキング処理
- [ID-2 Identity Federation & OBO](../id-identity/id2-identity-federation-obo.md) — 補完：検索時に本人権限で SaaS を呼ぶ委譲トークン
