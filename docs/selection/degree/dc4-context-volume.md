---
title: "DC-4 コンテキスト投入量（top-k・トークン予算）"
description: "RAG等で取得したコンテキストをどれだけプロンプトに投入するか、目的限定で最小化する連続量パラメータ。"
status: done
---

# DC-4 コンテキスト投入量（top-k・トークン予算）

## 概要

RAG で社内文書を 50 件取得できたとして、それを全部プロンプトに詰め込めば精度が上がるわけではない。トークンの大量消費、レイテンシ悪化に加え、中盤の情報が無視される「lost in the middle」現象で、むしろ回答品質が下がることもある。「使えるデータ」ではなく「このタスクに必要な最小のデータ」で絞る（[KM-5 Purpose-Bound Context](../../patterns/km-knowledge/km5-purpose-bound-context.md)）ために、top-k やトークン予算をどう設定するかを扱う。

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（少なすぎ） | top-k が小さすぎ、関連文脈が欠落 | 回答品質が低下し、幻覚が増加する |
| 過大（多すぎ） | 取得可能なデータを全件投入 | 精度低下（lost in the middle 現象）、コスト増、レイテンシ悪化、不要な機密情報の拡散 |

## 判断基準

- 関連度ランキングで上位のみを選択し、リランカーで件数をさらに絞る
- 目的別のトークン予算を設定し、予算内に圧縮する。タスクの種類（Q&A・要約・分析）で必要量は異なる
- [KM-5](../../patterns/km-knowledge/km5-purpose-bound-context.md) の目的限定原則に従い、タスクに不要な属性・フィールドは投入しない
- 機密度の高い情報は [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) でマスキング後に投入する

## 調整の仕組み

- [GV-7 Evaluation Pipeline](../../patterns/gv-governance/gv7-evaluation-governance-pipeline.md) で回答品質と投入量の相関を計測する
- top-k やトークン予算の値を段階的に変えた A/B テストで最適点を探る
- [OB-1](../../patterns/ob-observability/ob1-observability-lake.md) でトークン消費量と品質スコアの推移を監視し、コスト対品質比を追跡する

## 関連パターン

- [KM-5 Purpose-Bound Context](../../patterns/km-knowledge/km5-purpose-bound-context.md) — 目的限定の原則
- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — 権限認識 RAG でのコンテキスト取得
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — フェデレーテッド取得でのコンテキスト量制御
- [KM-6 DLP & Redaction Boundary](../../patterns/km-knowledge/km6-dlp-redaction-boundary.md) — 投入前のマスキング
