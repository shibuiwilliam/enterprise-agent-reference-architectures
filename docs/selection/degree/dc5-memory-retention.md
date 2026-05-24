---
title: "DC-5 メモリ保持・忘却（TTL・スコープ）"
description: "エージェントの記憶をどの程度保持し、いつ忘却するかをTTL・スコープ・ライフサイクルで決める連続量パラメータ。"
status: done
---

# DC-5 メモリ保持・忘却（TTL・スコープ）

## 概要

エージェントが「前回の会話の続き」を覚えていればパーソナライズが効くが、退職した社員の業務記録や、終了したプロジェクトの機密メモをいつまでも保持していれば、それは漏洩リスクの塊になる。「何をどのくらいの期間覚えておくか」「いつ忘れさせるか」を、セッション・個人・プロジェクト・組織の各スコープ（[KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)）ごとに設計する方法を扱う。

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（すぐ忘れる） | セッション終了で全消去 | 毎回同じ説明が必要になり、パーソナライズの価値が消える |
| 過大（すべて覚える） | 全記憶を無期限保持 | 古い情報に基づく誤判断、退職者のデータ残留、ストレージコスト増大 |

## 判断基準

- **重要度 × 鮮度 × 参照頻度**の3軸で残すものを選別する。古い詳細は要約へ圧縮する
- [KM-4](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) のスコープ（セッション・個人・プロジェクト・組織）ごとに TTL と失効条件を設定する
- **ライフサイクルイベントとの連動**：プロジェクト終了・退職・異動でメモリと権限を失効させる
- **本人の消去権**：本人がメモリを削除・修正できる権利を設計に含める（[ID-8](../../patterns/id-identity/id8-consent-access-transparency.md)）

## 調整の仕組み

- メモリの参照頻度・鮮度を [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) で計測し、未参照のメモリを自動アーカイブ・削除する
- 人事システム（異動・退職）との連携で、不要メモリの自動失効を実装する
- メモリ量とタスク品質の相関を [GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) で評価し、保持ポリシーを調整する

## 関連パターン

- [KM-4 Scoped Memory Hierarchy](../../patterns/km-knowledge/km4-scoped-memory-hierarchy.md) — スコープ記憶階層の設計本体
- [ID-8 Consent & Access Transparency](../../patterns/id-identity/id8-consent-access-transparency.md) — 消去権・透明化の原則
- [RT-11 Project Digital Twin](../../patterns/rt-runtime/rt11-project-digital-twin.md) — プロジェクトスコープの記憶管理
- [TO-6 個人の記憶 vs プロジェクト/チームの記憶](../tradeoff/to6-personal-vs-team-memory.md) — 個人 vs 共有の判断軸
