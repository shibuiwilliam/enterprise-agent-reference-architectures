---
title: "TO-6 個人の記憶 vs プロジェクト/チームの記憶"
description: "Personal EnclaveとProject Workspaceを物理・論理的に分離し、共有スコープを組織グラフに従わせることで漏洩と混線を防ぐ設計指針。"
status: done
---

# TO-6 個人の記憶 vs プロジェクト/チームの記憶

## 概要

「あの人が前に教えてくれたやり方」をエージェントが覚えていれば便利だ。しかし「あの人」が異動して別チームに移ったあとも、元チームのエージェントが個人の業務メモにアクセスできたらどうなるか。個人の効率化に使うメモリと、チーム全体で共有するプロジェクト知識は物理的・論理的に分離しなければ、漏洩と混線の温床になる。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: TO-6
decision_rules:
  - condition: "information_type IN ['personal_preferences', 'personal_notes', 'confidential_personal']"
    recommendation: personal_enclave
    reason: "個人設定・個人メモ・業務スタイル・機密情報は本人のみがアクセスできる個人Enclaveに保持する"
  - condition: "information_type IN ['shared_knowledge', 'project_documents', 'team_decisions']"
    recommendation: project_workspace
    reason: "共有ナレッジ・作業履歴・プロジェクト文書はプロジェクトWorkspaceに置き、組織グラフに従うACLで制御する"
  - condition: "single_store_for_all == true"
    recommendation: hybrid_separated
    reason: "個人メモとして書いた機密事項がチームメンバー全員に見えてしまうアンチパターンを防ぐため、物理・論理分離が必須"
  - condition: "user_transfers_team == true OR project_ends == true"
    recommendation: hybrid_separated
    reason: "プロジェクト終了・退職・異動でメモリと権限を失効させる。組織グラフとの同期でメンバー変更が自動的にアクセス権に反映される"
  - condition: "information_type == 'hr_performance_salary_medical'"
    recommendation: personal_enclave
    reason: "個人のパフォーマンス評価・給与情報・医療情報は、たとえプロジェクト文書として作成されても共有領域に入れてはならない"
```

## 比較

| 観点 | Personal Enclave（個人領域） | Project Workspace（共有領域） |
|---|---|---|
| 帰属 | 個人 | プロジェクト・チーム・部門 |
| アクセス可能者 | 本人のみ | プロジェクトメンバー |
| 含む情報 | 個人設定・個人メモ・業務スタイル・機密情報 | 共有ナレッジ・作業履歴・プロジェクト文書 |
| 管理パターン | [KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) | [RT-11](../../patterns/rt-runtime/rt11-project-digital-twin.md) |
| 分離方式 | 物理分離（別ストレージ）または強い論理分離 | 組織グラフに従うACL |

## 判断基準

個人の効率化には個人メモリ、サイロ化防止には共有メモリが必要だ。しかしこの二つを同一ストアで管理すると、個人の機密情報がプロジェクト共有領域に混入するリスクが生じる。

**Personal EnclaveとProject Workspaceは物理的または論理的に分離**（[KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) / [RT-11](../../patterns/rt-runtime/rt11-project-digital-twin.md)）することを基本とする。

共有スコープの決定基準：

- **組織グラフに従う**：誰がプロジェクトメンバーかは組織の権限管理システム（IdP・HR システム）から取得する。エージェントやユーザーが任意にスコープを変更できてはならない
- **プロジェクト終了時に棚卸しを行う**：終了後、共有領域に残った情報の保持継続・アーカイブ・削除を明示的に決定する
- **個人情報は共有領域に書き込まない**：個人のパフォーマンス評価・給与情報・医療情報は、たとえプロジェクト文書として作成されても共有領域に入れてはならない

一本化が招くアンチパターン：

- 個人メモとして書いた機密事項がチームメンバー全員に見えてしまう
- 複数プロジェクトの記憶が混在し、エージェントが誤ったプロジェクト情報を回答に使う
- 退職者の個人記憶が組織の共有ストアに残り続ける

## ハイブリッド・段階的アプローチ

ユーザーが意識せずに適切なスコープへ記憶が書き込まれる仕組みが理想だ。

1. まず個人Enclaveのみを実装し、全記憶を個人スコープで保持する。
2. プロジェクト単位でProject Workspaceを追加し、明示的な「共有」操作でのみ個人→共有に移動できるようにする。
3. 組織グラフとの同期（[ID-8](../../patterns/id-identity/id8-consent-access-transparency.md)）を整備し、メンバー変更が自動的にアクセス権に反映されるようにする。
4. 記憶の有効期限（[KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)のTTL）を設定し、古い情報が蓄積し続けない設計にする。

## 関連パターン

- [KM-4 Scoped Memory Hierarchy](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)
- [RT-11 Project Digital Twin](../../patterns/rt-runtime/rt11-project-digital-twin.md)
- [ID-8 Consent & Access Transparency](../../patterns/id-identity/id8-consent-access-transparency.md)
