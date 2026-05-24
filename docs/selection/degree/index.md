---
title: "「程度」の選定基準"
description: "自律度・予算・ログ粒度・コンテキスト量・メモリ保持・ガードレール強度など連続量パラメータの決め方。"
status: done
---

# 「程度」の選定基準

連続量パラメータは、過小・過大の両極が害になる。本番トレース（[OB-1](../../patterns/ob-observability/ob1-observability-lake.md)）と評価（[GV-7](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)）で継続調整する前提で、出発点と判断軸を示す。

| ID | 名称 | 概要 |
|---|---|---|
| [DC-1](dc1-risk-tier-boundary.md) | 自律度のティア境界 | Risk-Tier の引き方。影響の不可逆性・額・機密度・職責で決定 |
| [DC-2](dc2-timeout-retry-budget.md) | タイムアウト・リトライ・予算 | コスト上限。遅く高コストなエージェントに予算制約を設ける |
| [DC-3](dc3-log-granularity.md) | ログ粒度 | 三層分離。メタ・本文・集計の保存先と粒度を使い分ける |
| [DC-4](dc4-context-volume.md) | コンテキスト投入量 | top-k・トークン予算。目的に必要な最小データで絞る |
| [DC-5](dc5-memory-retention.md) | メモリ保持・忘却 | TTL・スコープ。重要度×鮮度×参照頻度で選別する |
| [DC-6](dc6-guardrail-strength.md) | ガードレール強度 | 誤検知 vs 見逃し。リスク経路ごとに閾値を可変にする |
| [DC-7](dc7-cache-jit-ttl.md) | キャッシュ積極度・JIT 資格情報 TTL | 誤ヒットの害と速度のトレードオフで調整する |
| [DC-8](dc8-model-routing.md) | モデルの強さ・データ分類別ルーティング | 難易度とデータ分類で経路を分ける |
| [DC-9](dc9-canary-event-throttle.md) | カナリア段階・イベント駆動の頻度制限 | 多段ロールアウトとイベント嵐の抑制 |
