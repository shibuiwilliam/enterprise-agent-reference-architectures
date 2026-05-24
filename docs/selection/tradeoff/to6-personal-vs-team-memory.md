---
title: "TO-6 個人の記憶 vs プロジェクト/チームの記憶"
description: "Personal EnclaveとProject Workspaceを物理・論理的に分離し、共有スコープを組織グラフに従わせることで漏洩と混線を防ぐ設計指針。"
status: done
---

# TO-6 個人の記憶 vs プロジェクト/チームの記憶

## 概要

エージェントが保持する記憶（コンテキスト・過去のやり取り・学習済み情報）は、個人に帰属するものとプロジェクト・チームに帰属するものを明確に分離する必要がある。一本化した記憶ストアは情報の漏洩と混線の温床になる。

## 比較

| 観点 | Personal Enclave（個人領域） | Project Workspace（共有領域） |
|---|---|---|
| 帰属 | 個人 | プロジェクト・チーム・部門 |
| アクセス可能者 | 本人のみ | プロジェクトメンバー |
| 含む情報 | 個人設定・個人メモ・業務スタイル・機密情報 | 共有ナレッジ・作業履歴・プロジェクト文書 |
| 管理パターン | [KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) | [RT-11](../../patterns/rt-runtime/rt11-project-digital-twin.md) |
| 分離方式 | 物理分離（別ストレージ）または強い論理分離 | 組織グラフに従うACL |

## 判断基準

個人の効率化には個人メモリ、サイロ化防止には共有メモリが必要である。しかしこの二つを同一ストアで管理すると、個人の機密情報がプロジェクト共有領域に混入するリスクが生じる。

**Personal EnclaveとProject Workspaceは物理的または論理的に分離**（[KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) / [RT-11](../../patterns/rt-runtime/rt11-project-digital-twin.md)）することを基本とする。

共有スコープの決定基準：

- **組織グラフに従う**：誰がプロジェクトメンバーかは組織の権限管理システム（IdP・HR システム）から取得する。エージェントやユーザーが任意にスコープを変更できてはならない。
- **プロジェクト終了時に棚卸しを行う**：プロジェクト終了後、共有領域に残った情報の保持継続・アーカイブ・削除を明示的に決定する。
- **個人情報は共有領域に書き込まない**：個人のパフォーマンス評価・給与情報・医療情報は、たとえプロジェクト文書として作成されても共有領域に入れてはならない。

一本化が招くアンチパターン：

- 個人メモとして書いた機密事項がチームメンバー全員に見えてしまう
- 複数プロジェクトの記憶が混在し、エージェントが誤ったプロジェクト情報を回答に使う
- 退職者の個人記憶が組織の共有ストアに残り続ける

## ハイブリッド・段階的アプローチ

ユーザーが意識せずに適切なスコープに記憶が書き込まれる仕組みが理想である。

1. まず個人Enclaveのみを実装し、全記憶を個人スコープで保持する。
2. プロジェクト単位でProject Workspaceを追加し、明示的な「共有」操作でのみ個人→共有に移動できるようにする。
3. 組織グラフとの同期（[ID-8](../../patterns/id-identity/id8-consent-access-transparency.md)）を整備し、メンバー変更が自動的にアクセス権に反映されるようにする。
4. 記憶の有効期限（[KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)のTTL）を設定し、古い情報が蓄積し続けない設計にする。

## 関連パターン

- [KM-4 Scoped Memory Hierarchy](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)
- [RT-11 Project Digital Twin](../../patterns/rt-runtime/rt11-project-digital-twin.md)
- [ID-8 Consent & Access Transparency](../../patterns/id-identity/id8-consent-access-transparency.md)
