---
title: "H-3 Prompt-Cache Optimized Context（プロンプトキャッシュ最適化）"
description: "共通プロンプトやツール定義をキャッシュしやすい構造にして入力トークンコストとレイテンシを下げるパターン。"
status: done
---

# H-3 Prompt-Cache Optimized Context（プロンプトキャッシュ最適化）

## 概要

共通プロンプトやツール定義をキャッシュしやすい構造にして、入力トークンコストとレイテンシを下げる。

## 設計

system prompt・tool definitions・policy・共通知識を安定したprefixとして固定し、ユーザー固有情報は後方に置く。プロバイダのprompt cachingを効かせる。

```mermaid
flowchart LR
    subgraph 安定prefix（キャッシュ対象）
        Sys[System Prompt]
        Tools[Tool Definitions]
        Policy[Policy]
    end
    subgraph 可変suffix
        User[ユーザー固有情報]
        Task[タスクコンテキスト]
    end
    安定prefix（キャッシュ対象） --> LLM[LLM]
    可変suffix --> LLM
```

## 解決する課題

- 長いsystem prompt・ツール定義・RAGコンテキストによる高コスト・高レイテンシ

## ユースケース

- 共通プロンプトが大きいエージェントプラットフォーム
- MCPツールが多い環境

## 向き

反復的に同一prefixを使う構成に適する。

## 不向き

毎回まったく異なる短いプロンプトには効果が薄い。

## 要素技術

- **設計**：prompt prefix design
- **キャッシュ**：provider prompt caching
- **効率化**：context hashing
- **遅延読込**：tool lazy loading

## 関連パターン

- [H-2 Semantic Result Cache](h2-semantic-cache.md) — 結果レベルのキャッシュ
- [E-2 Context Pack](../e-memory/e2-context-pack.md) — コンテキストの構成管理
- [H-1 Cost-Aware Model Router](h1-cost-aware-router.md) — コスト最適化の全体戦略
- [D-1 Tool Gateway](../d-tools-mcp/d1-tool-gateway.md) — ツール定義の管理
