---
title: "「相反する仕組み」の選定基準"
description: "同期/非同期・単一/複数エージェントなど、AIエージェント設計で頻出する二者択一の判断軸と選定基準を体系化する。"
status: done
---

# 「相反する仕組み」の選定基準

設計では二者択一に見える対立が頻出する。実務の答えは多くの場合「どちらか一方」でなく「**どこで線を引くか**」である。各軸について判断基準を示す。

## 5.1 同期 vs 非同期

| 判断軸 | 同期を選ぶ | 非同期を選ぶ（[A-1](../patterns/a-execution/a1-request-to-job-gateway.md)/[A-2](../patterns/a-execution/a2-durable-session.md)） |
|---|---|---|
| 処理時間 | 数秒以内で収まる | 数十秒〜数分以上 |
| UX | 対話的に即応が必要 | 完了後の通知で足りる |
| 失敗時コスト | やり直しが安い | 途中失敗の再実行が高い→耐久セッション併用 |
| 接続維持 | コネクション保持が現実的 | 保持コスト/タイムアウトが問題化 |

**基準**：チャットの単発応答は同期＋ストリーミング（[A-3](../patterns/a-execution/a3-streaming-progress.md)）で体感改善。バックグラウンドの複数ステップ自律タスクは非同期＋ジョブ＋耐久セッション。**ハイブリッド**（即時に部分結果をストリーム、重い処理を非同期化して後追い通知）が実用上の最適解になりやすい。

## 5.2 シングルエージェント vs マルチエージェント

| 判断軸 | シングル | マルチ（[B-2](../patterns/b-composition/b2-planner-executor-reviewer.md)/[B-3](../patterns/b-composition/b3-supervisor-specialist.md)/[B-5](../patterns/b-composition/b5-blackboard.md)） |
|---|---|---|
| タスク構造 | 単一責務で完結 | 明確に分解でき専門性が分かれる |
| プロンプト | 1つに収まる | 1プロンプトが肥大し精度低下 |
| コスト/レイテンシ | 制約が厳しい | 余裕があり品質優先 |
| デバッグ | 単純さ優先 | 複雑な協調を許容できる |

**基準**：**まずシングルで始める**。「責務過多で精度が落ちる」「並列化で速度/専門性の利得が明確」になって初めてマルチへ。マルチはコスト・レイテンシ・協調の複雑性・障害点を増やす。**安易なマルチ化は解決する問題より作る問題が多い**。

## 5.3 汎用 vs 専門エージェント

**基準**：入力種別が多様で各々別処理が要る → ルーター＋専門群（[B-3](../patterns/b-composition/b3-supervisor-specialist.md)）。入力が一様 → 単一汎用。専門化はコンテキストを絞れて精度・コストで有利だが、種類増で管理コストとルーティング誤りが増える。能力レジストリ（[J-3](../patterns/j-abstraction/j3-capability-registry.md)）で選定根拠を管理する。

## 5.4 集中型オーケストレーション vs 分散型協調

**基準**：制御・監査・予測可能性が重要 → 集中型（オーケストレーター/ステートマシン、[B-1](../patterns/b-composition/b1-deterministic-backbone.md)/[B-2](../patterns/b-composition/b2-planner-executor-reviewer.md)）。動的・探索的でどの専門家がいつ要るか事前に決められない → 分散型（ブラックボード/イベント駆動、[B-5](../patterns/b-composition/b5-blackboard.md)）。本番業務は概ね集中型が安全。分散型は柔軟だがデバッグ・保証が難しい。

## 5.5 決定論的バックボーン vs 自律エージェント

**基準**：状態遷移・権限・金額計算・DB更新は決定論コードに残し、曖昧処理・生成・探索だけをエージェントに委ねる（[B-1](../patterns/b-composition/b1-deterministic-backbone.md)）。委任度は「**誤りの不可逆性とコスト**」で決める。規制・監査が重い領域ほど決定論側に寄せ、探索的研究・創作ほどエージェント側に寄せる。

## 5.6 フレームワーク利用 vs 自前実装

**基準**：標準パターンを素早く立ち上げたい → フレームワーク（LangGraph/CrewAI/Agents SDK）。細かい制御・性能・依存最小化・長期保守が重要 → 薄い自前実装。エージェント領域は進化が速くロックインリスクがあるため、**コア制御フローは自前 or 薄い抽象（[J-1](../patterns/j-abstraction/j1-runtime-abstraction.md)）、周辺（観測・評価）はツール活用**の折衷が堅実。

## 5.7 プロバイダ抽象化 vs プロバイダ固有最適化

**基準**：マルチプロバイダ・フェイルオーバー・移行容易性が重要 → 抽象化（[J-1](../patterns/j-abstraction/j1-runtime-abstraction.md)/[J-2](../patterns/j-abstraction/j2-model-compatibility-layer.md)、最大公約数のインターフェイス）。特定モデル固有機能（prompt caching、structured outputs、特殊ツール）で性能/コストを絞り出したい → 固有最適化。両立策：抽象化を基本としつつ、ホットパスだけ固有機能を「逃がし口」で使う。

## 5.8 RAG vs ロングコンテキスト vs ファインチューニング

| 手段 | 向く | 不向き |
|---|---|---|
| RAG（[F-1](../patterns/f-reliability/f1-evidence-first.md)） | 知識が大量・更新頻繁・出典が要る | 推論力が主役/検索精度が出ない |
| ロングコンテキスト | 文書が中規模で毎回全体が要る | 巨大/高頻度（コスト・精度劣化） |
| ファインチューニング | 様式・口調・形式の固定化、専門タスク反復 | 知識の鮮度が要る/データが少ない |

**基準**：鮮度・出典が要る→RAG。振る舞い/様式の固定化→FT。排他でなく**併用**が普通（FTで様式、RAGで知識）。

## 5.9 事前検証 vs 事後検証

**基準**：入力の不正・インジェクション・トピック逸脱 → 事前（入力ガード、[F-2](../patterns/f-reliability/f2-guardrail-sidecar.md)）。出力の形式・事実・安全性 → 事後（出力ガード＋再生成、[F-3](../patterns/f-reliability/f3-verifier-agent.md)）。事前で弾ければLLM呼び出しを節約できるが、事後でしか分からない品質問題も多い。**両方を薄く併置**が基本。

## 5.10 ステートレス vs ステートフル

**基準**：1回完結・スケール容易性優先 → ステートレス。長期対話・継続パーソナライズ → 実質ステートフルだが、**状態は外部メモリ（[E-1](../patterns/e-memory/e1-layered-memory.md)）/耐久セッション（[A-2](../patterns/a-execution/a2-durable-session.md)）に持たせ、エージェント本体はステートレスに保つ**（水平スケールしやすい）のが定石。

## 5.11 早期（eager）vs 遅延（lazy）ツール実行

**基準**：必要性が確実なら早期に並列実行してレイテンシ短縮。必要か不確実・高コスト・副作用ありなら遅延（必要と確定してから）。**副作用ツールは原則レイジー＋承認ゲート（[D-3](../patterns/d-tools-mcp/d3-dry-run-execution.md)/[F-5](../patterns/f-reliability/f5-human-approval.md)）**。

## 5.12 構造化出力 vs 自然言語出力

**基準**：下流が機械処理（基幹連携・ツール引数）→ 構造化必須（[C-2](../patterns/c-io-contract/c2-structured-output-contract.md)、JSON Schema＋検証）。最終的に人間が読む対話 → 自然言語。境界（[C-1](../patterns/c-io-contract/c1-nl-boundary-adapter.md)/[L-2](../patterns/l-adoption/l2-anti-corruption-layer.md)）で「**内側は構造化、外側は自然言語**」と層を分けるのが実用的。

## 5.13 自前/オンプレモデル vs API/マネージド

**基準**：データ主権・コンプラ・大量定常トラフィックのコスト → 自前/オンプレ。最新性能・運用負荷最小・変動トラフィック → API。可用性は外因依存のため、APIは**フォールバック前提**（[H-4](../patterns/h-cost-performance/h4-graceful-degradation.md)）で。

## 5.14 自己検証 vs 独立検証器

**基準**：自己採点は甘くなりがち。誤りコストが高いほど**生成器と独立な検証器**（できれば決定論的、[F-3](../patterns/f-reliability/f3-verifier-agent.md)）を置く。低リスクの内部メモなら自己検証で十分。

## 5.15 アンサンブル（N並列）vs 単発

**基準**：正誤が判定可能で誤りコストが高い高価値タスク → アンサンブル/best-of-N（[B-4](../patterns/b-composition/b4-ensemble-debate.md)）。コスト・レイテンシ制約が厳しい大量処理 → 単発。難問のみNを増やす適応制御が現実的。

## 5.16 プロンプトで守る vs ポリシー/実行基盤で守る

**基準**：この軸の答えは明確で、**プロンプトはセキュリティ境界にならない**。権限・承認・検証・隔離・ポリシー（[D-2](../patterns/d-tools-mcp/d2-least-privilege-binding.md)/[F-4](../patterns/f-reliability/f4-policy-as-code.md)/[F-5](../patterns/f-reliability/f5-human-approval.md)/G系/[L-3](../patterns/l-adoption/l3-agent-constitution.md)）で守る。プロンプトは品質・ふるまいの調整に使い、安全保証は実行基盤側に置く。
