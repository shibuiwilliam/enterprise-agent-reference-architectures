---
title: "DC-9 カナリア段階・イベント駆動の頻度制限"
description: "カナリアリリースの段階設計とイベント駆動エージェントの頻度制限を設計する連続量パラメータ。"
status: done
---

# DC-9 カナリア段階・イベント駆動の頻度制限

## 概要

エージェントの新バージョン展開をカナリア方式で段階的に進める際の刻み幅と、[RT-10 Event-Driven Orchestrator](../../patterns/rt-runtime/rt10-event-driven-orchestrator.md) でのイベント頻度制限をどう設計するかを決める連続量パラメータである。展開速度と安全性のバランス、およびイベントストーム抑制の粒度を扱う。

## 過小・過大の害

**カナリアリリース**

| 極 | 状態 | 害 |
|---|---|---|
| 過小（段階が細かすぎ・速度が遅すぎ） | 1%→2%→3%…と刻む | 新バージョンの展開に時間がかかりすぎ、サンプル数が少なくて統計的有意差が得られない |
| 過大（段階が大きすぎ・速度が速すぎ） | 初回から50%以上に展開 | 問題を検出する前に影響が広がり、ロールバックのコストが高くなる |

**イベント頻度制限**

| 極 | 状態 | 害 |
|---|---|---|
| 過小（制限なし） | イベントをすべてエージェントに即時配信 | イベントストームが発生し、推論コストが急増する。依存システムも過負荷になる |
| 過大（制限が厳しすぎ） | 大半のイベントを間引く | 必要なイベントが欠落し、エージェントが古い状態で判断を続ける |

## 判断基準

**カナリアリリースの段階設計**

- 1% → 5% → 25% → 100% の多段階を基本とし、各段階でトラフィックを十分に収集してから次へ進む
- 品質スコア・コスト・エラー率のいずれかが閾値を下回った段階で [GV-6 Version Registry & Rollback](../../patterns/gv-governance/gv6-version-registry.md) の自動ロールバックを発動する
- トラフィック量が少なく統計的有意差が得にくい場合は、オフライン評価（[GV-7 Evaluation Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）で補完してから次段階へ進む判断を行う

**イベント駆動の頻度制限**

- デバウンス（短時間に連続発生したイベントをまとめる）、頻度上限（単位時間あたりの処理件数の上限）、予算上限（セッション予算消費量の上限）の3つを組み合わせる
- 同一ソースから大量のイベントが流入するイベントストーム時は、頻度上限を超えたイベントをキューに退避するか、サンプリングで間引く
- 頻度制限のパラメータは、イベントの業務重要度と推論コストを考慮して種別ごとに設定する

## 調整の仕組み

- [GV-6 Version Registry & Rollback](../../patterns/gv-governance/gv6-version-registry.md) の展開ステータスと連動し、各段階の品質指標を自動収集・判定する
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) のオフライン評価を各段階の判断に活用し、本番トラフィックが少ない段階での意思決定を補強する
- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でイベント処理量・スキップ量・エラー率を計測し、頻度制限パラメータの過大・過小を検出する
- イベントストームの発生パターンを分析し、デバウンス時間窓と頻度上限を業務サイクル（日次バッチ・月次締め処理など）に合わせて調整する

## 関連パターン

- [GV-6 Version Registry & Rollback](../../patterns/gv-governance/gv6-version-registry.md) — カナリア展開と自動ロールバックの実装本体
- [GV-7 Evaluation & Governance Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) — オフライン評価によるカナリア判断の補完
- [RT-10 Event-Driven Orchestrator](../../patterns/rt-runtime/rt10-event-driven-orchestrator.md) — イベント駆動エージェントの実行制御
