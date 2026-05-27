---
title: "KM-4 Scoped Memory Hierarchy（スコープ記憶階層）"
description: "メモリを個人/チーム/プロジェクト/部門/全社/顧客/エージェント内部に分離し、共有範囲を組織グラフに従わせるパターン。"
status: done
pattern_id: KM-4
facet: knowledge
requires: []
required_by: []
applies_when: [continuous_use_spanning_multiple_departments_or_projects, agents_handling_customer_information, long_term_projects_where_context_accumulation_is_important]
not_applicable_when: [completely_stateless_one_off_use, read_only_reference_ai_without_memory_needed, one_time_question_answer_sessions]
risk_tiers: [2, 3]
key_technologies: [Memory Store, "Vector DB (Namespace isolation)", ACL, TTL, Memory Review UI]
---

# KM-4 Scoped Memory Hierarchy（スコープ記憶階層）

## 概要

エージェントにメモリを持たせると便利だが、「個人のメモリがチーム全体に見える」「A プロジェクトの顧客情報が B プロジェクトに漏れる」という事故が起きる。このパターンはメモリを個人・チーム・プロジェクト・部門・全社・顧客の各スコープに分離し、共有範囲を組織グラフに従わせる。退職やプロジェクト終了に連動してメモリと権限を自動で失効させ、本人が自分のメモリを消去できる権利も設計に含める。

## 解決する企業課題

エージェントにメモリを持たせると過去の文脈を再利用できる反面、「誰がどの記憶を参照できるか」を管理しなければ情報漏洩の経路になる。個人メモリがチーム全体に見える、A プロジェクトで得た顧客情報が B プロジェクトのエージェントに参照される、退職した担当者が持っていた文脈が後任に見える——これらはスコープなし設計で発生する典型的な問題だ。

企業の組織構造はそれ自体が情報共有の権威ある基準だ。「同じチームのメンバーは同じ情報を見てよい」「部門長は部門内のプロジェクト情報を見てよい」という組織の論理をメモリ階層に反映させることで、権限管理を組織グラフという既存の権威ソースに委ねられる。プロジェクト終了・退職・異動といったライフサイクルイベントに連動してメモリを失効させることで、陳腐化した文脈の誤用も防げる。

!!! tip "最小成立条件（MVP）"
    Vector DB の Namespace を Personal / Team / Company の3層に分け、書き込み時にスコープを付与する。組織グラフ連動や自動失効は後続フェーズでよいが、スコープ分離だけは初期から入れる。

## 価値仮説

チーム・プロジェクト単位の記憶共有により、ナレッジの属人化を解消する。暗黙知の共有は新人の立ち上がり時間短縮とチーム生産性向上に寄与する。

## 解決策と設計

各スコープを物理的・論理的に分離し、書き込みはゲート（分類・重複検知・承認）を通す。サブプロジェクトは親の非機密情報のみ継承し、承認者は種別ごとに異なる（PM / 部門責任者 / 顧客情報管理者）。

```mermaid
flowchart TB
    subgraph Scope["メモリスコープ"]
        PERSONAL[Personal Enclave<br/>本人のみ]
        TEAM[Team Memory<br/>チーム]
        PROJECT[Project Workspace<br/>プロジェクト＋上位]
        DEPT[Department Memory<br/>部門]
        COMPANY[Company Memory<br/>全社]
        CUSTOMER[Customer Memory<br/>担当者・許可者]
    end

    subgraph Gate["書き込みゲート"]
        CLASS[分類]
        DUP[重複検知]
        APPROVE[承認]
    end

    subgraph OrgGraph["組織グラフ"]
        ORG[スコープ・共有範囲の<br/>権威ソース]
    end

    Gate --> Scope
    ORG --> Scope
```

スコープの境界は Vector DB の Namespace や暗号化キーで物理的に分離する。プロジェクト終了・退職・異動でメモリと権限を失効させる処理を自動化する。本人が自分のメモリを確認・消去できる Memory Review UI を提供し、Right to Erasure（消去権）を設計に組み込む。

## 向き／不向き

| 向き | 不向き |
|---|---|
| 継続利用・複数部署/プロジェクトに跨がる AI | 完全ステートレスの単発利用 |
| 顧客情報を扱うエージェント | メモリ不要の参照専用 AI |
| 長期プロジェクトで文脈蓄積が重要 | 一回限りの質問応答 |

## 要素技術・既存システム連携

- **ストレージ**：Memory Store、Vector DB（Namespace 分離）
- **アクセス制御**：ACL、Namespace、スコープ別暗号化
- **寿命管理**：TTL、Consent（本人の消去権）、ライフサイクル失効
- **レビュー**：Memory Review UI（蓄積内容の確認・修正）
- **組織グラフ**：Workday/Okta からのスコープ導出

## 落とし穴／選定の勘所

!!! warning "全社共有メモリの罠"
    すべてを「全社共有メモリ」にし機密と雑多を混在させるのは最大のアンチパターンである。スコープを分離し、共有範囲を組織グラフに従わせる。「速く作れるから全部共有」は技術負債ではなくセキュリティ上の欠陥である。

- 本人が自分のメモリを確認・消去できる権利（Right to Erasure）を設計に含める。規制要件（GDPR 等）への対応だけでなく、誤った情報が蓄積した場合の修正手段としても必要である。
- プロジェクト終了時のメモリアーカイブ/失効を自動化する。放置すると異動者経由で元のプロジェクト情報が漏洩する。
- メモリの保持・忘却は「重要度 × 鮮度 × 参照頻度」で選別し、古い詳細は要約へ圧縮する。無限に蓄積するとノイズが増え、有用な文脈の検索精度が下がる。

## Interfaces

以下はこのパターンを実装する際の主要インターフェイスである。コーディングエージェントはこの定義からスタブコードを生成できる。

```yaml
interfaces:
  - name: Memory Scope Partitioner
    description: "Physically or logically separates memory by scope using Vector DB namespaces or encryption keys; writes pass through a classification and duplicate-detection gate."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Memory Scope Partitioner の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
  - name: Lifecycle Event Handler
    description: "Listens for org events (project closed, employee departed, transfer) and triggers memory archive/expiry and RBAC group removal automatically."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Lifecycle Event Handler の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
  - name: Memory Review UI
    description: "Allows individuals to inspect, correct, and erase their personal memory scope to satisfy Right to Erasure requirements."
    input:
      request: object
    output:
      response: object
    errors:
      - code: GENERAL_ERROR
        description: "Memory Review UI の処理中にエラーが発生"
    protocol: "REST / gRPC"
    implementation_hints:
      - "詳細は本文の「解決策と設計」節を参照"
```

## 関連パターン

- [KM-3 Canonical Object & Knowledge Graph](km3-canonical-object-knowledge-graph.md) — 補完：組織グラフの構築とスコープ導出の基盤
- [KM-5 Purpose-Bound Context](km5-purpose-bound-context.md) — 補完：メモリから取り出す文脈を業務目的でさらに限定する
- [RT-11 Project Digital Twin](../rt-runtime/rt11-project-digital-twin.md) — 類似：プロジェクトスコープの共有メモリと状態管理
- [ID-8 Consent & Access Transparency](../id-identity/id8-consent-access-transparency.md) — 補完：メモリへのアクセスに対する本人の同意と透明化
- [ID-4 Permission Mirror](../id-identity/id4-permission-mirror-least-of.md) — 補完：メモリアクセスの権限評価と最小権限の適用
