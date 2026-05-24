---
title: "G-2 Data Boundary Firewall（データ境界ファイアウォール／DLP）"
description: "LLMに渡す前後でデータを検査・マスキング・分類し、過剰送信と機密流出を防ぐパターン。"
status: done
---

# G-2 Data Boundary Firewall（データ境界ファイアウォール／DLP）

## 概要

LLMに渡す前後でデータを検査・マスキング・分類し、過剰送信と機密流出を防ぐ。

## 設計

入力時にPII・機密・契約・認証情報を検出し、渡してよい情報だけをredaction/tokenizationして渡す。出力時もegress filterで機密混入を検査する。

```mermaid
flowchart LR
    Input[入力データ] --> Ingress[Ingress Filter<br>PII検出・マスキング]
    Ingress --> LLM[LLM処理]
    LLM --> Egress[Egress Filter<br>機密混入検査]
    Egress --> Output[出力]
```

## 解決する課題

- LLMへの過剰データ送信
- 出力への秘密混入
- 越境データ問題

## ユースケース

- 個人情報・顧客情報を扱うAI
- 営業秘密・ソースコードを扱うAI

## 向き

機密データを扱うすべてのエージェントに適する。

## 不向き

公開情報のみを扱うAIには過剰である。

## 要素技術

- **データ保護**：DLP
- **検出**：PII detector
- **マスキング**：redaction、tokenization
- **分類**：data classification
- **出力制御**：egress filter

## 関連パターン

- [G-1 Confused-Deputy Damage Limitation](g1-confused-deputy-limitation.md) — 信頼できない入力の分離
- [F-2 Guardrail Sidecar](../f-reliability/f2-guardrail-sidecar.md) — 入出力ガードレールとの連携
- [G-3 Tenant-Isolated Runtime](g3-tenant-isolated-runtime.md) — テナント間のデータ分離
- [E-3 Memory Write Gate](../e-memory/e3-memory-write-gate.md) — メモリへの機密書き込み防止
