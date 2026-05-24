---
title: "DC-2 タイムアウト・リトライ・予算（コスト上限）"
description: "エージェントのタイムアウト・リトライ回数・セッションコスト上限を決める連続量パラメータ。"
status: done
---

# DC-2 タイムアウト・リトライ・予算（コスト上限）

## 概要

エージェントは従来の API に比べて桁違いに遅く、1回のセッションで数百円のトークンコストがかかることもある。タイムアウトを短くしすぎれば正当な処理が途中で打ち切られ、制限を緩めすぎれば無限ループで高額請求が発生する。「何秒待つか」「何回リトライするか」「1セッションいくらまで使ってよいか」の3つの上限をどう設定するかを扱う。

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（厳しすぎ） | タイムアウトが短すぎ、リトライ不可、予算が少なすぎ | 正当な処理が途中で打ち切られ、タスク完了率が低下する |
| 過大（緩すぎ） | タイムアウトが長すぎ、無制限リトライ、予算上限なし | 無限ループ・暴走による高額請求、リソース占有が発生する |

## 判断基準

- **タイムアウト**：TTFT（Time to First Token）と全体タイムアウト（無進捗時間）を別に設定する。TTFT はモデル応答の生死判定、全体タイムアウトは処理が進行しているかの判定に使う
- **リトライ**：冪等なステップのみリトライ対象にする。指数バックオフ＋ジッタで最大2〜3回に制限する。非冪等な操作（書き込み・送信）のリトライは二重実行の害が大きい
- **セッション予算**：コスト（トークン消費額）と時間（経過時間）の両面で上限を設ける。セッション全体の予算に各ステップを従属させる
- **マルチエージェント構成**：[RT-2 RACI-based Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md) では推論コストが N 倍になるため、予算上限を厳格にする

## 調整の仕組み

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でセッション単位のコスト・所要時間・リトライ回数・タイムアウト発生率を計測する
- [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) の部門別予算と連動させ、予算超過時の挙動（停止・縮退・承認昇格）を定義する
- タイムアウト率が高い処理はタスク分割や非同期化（[RT-8](../../patterns/rt-runtime/rt8-durable-workflow.md)）を検討する

## 関連パターン

- [RT-2 RACI-based Multi-Agent](../../patterns/rt-runtime/rt2-raci-multi-agent.md) — マルチエージェントでのコスト増加
- [RT-8 Durable Workflow](../../patterns/rt-runtime/rt8-durable-workflow.md) — タイムアウトを超える長時間処理の対策
- [GV-8 Cost Quota & Chargeback](../../patterns/gv-governance/gv8-cost-quota-chargeback.md) — 予算管理・配賦の仕組み
- [GV-9 Incident Response & Kill Switch](../../patterns/gv-governance/gv9-incident-response-kill-switch.md) — 暴走時の強制停止
