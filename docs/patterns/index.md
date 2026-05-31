---
title: パターン索引
status: done
---

# パターン索引（機械可読・一次フィルタ）

要件に合う「トリガ」を探し、リンクから各パターンへ。詳細フィールドの意味は
[パターン記述フォーマット規約](../usage/pattern-schema.md) を参照。

| ID | パターン | カテゴリ | 対象 | 成熟度 | 主なトリガ |
|----|---------|---------|------|--------|-----------|
| [P01](trust-boundary/p01-trust-boundary-split.md) | 信頼境界の二層分離 | 信頼境界 | 両方 | 基盤 | 顧客と従業員が同居 |
| [P02](trust-boundary/p02-multi-tenant-isolation.md) | マルチテナント分離 | 信頼境界 | 顧客 | 基盤 | 数万顧客・テナント混在 |
| [P03](integration/p03-ai-gateway.md) | AIエージェント・ゲートウェイ | 統合 | 両方 | 基盤 | 全社AI解禁・複数モデル |
| [P04](integration/p04-mcp-gateway.md) | MCPゲートウェイ/ツール連合 | 統合 | 両方 | 標準 | SaaSが10種以上 |
| [P06](integration/p06-agent-hub.md) | エージェント・ハブ | 統合 | 両方 | 標準 | 横断業務・入口一本化 |
| [P07](integration/p07-event-driven-agent.md) | イベント駆動エージェント | 統合 | 両方 | 標準 | 予防対応・24/365・一次対応 |
| [P08](identity/p08-token-exchange-obo.md) | トークン交換(OBO) | ID/認可 | 両方 | 基盤 | 複数SaaSをユーザー権限で操作 |
| [P09](identity/p09-dynamic-authz-pdp.md) | 動的認可(PDP/PBAC) | ID/認可 | 両方 | 標準 | 操作の影響度が幅広い |
| [P10](identity/p10-context-firewall.md) | コンテキスト・ファイアウォール | ID/認可 | 両方 | 標準 | 複数ソースを混ぜたコンテキスト |
| [P11](identity/p11-zero-trust-sandbox.md) | ゼロトラスト/サンドボックス | ID/認可 | 両方 | 高度 | コード実行・自動アクション |
| [P12](memory/p12-layered-memory.md) | 階層化メモリ | メモリ | 両方 | 標準 | セッション/エージェント跨ぎ |
| [P14](memory/p14-semantic-layer.md) | セマンティックレイヤー/知識グラフ | メモリ | 両方 | 標準 | 指標/用語/組織の曖昧性解消 |
| [P15](orchestration/p15-single-vs-multi.md) | シングル vs マルチエージェント | オーケストレーション | 両方 | 標準 | 複雑度・専門分離の判断 |
| [P16](orchestration/p16-supervisor-router.md) | スーパーバイザ/ルーター | オーケストレーション | 両方 | 標準 | 意図分類して委譲 |
| [P17](orchestration/p17-deterministic-workflow-hybrid.md) | エージェント＋決定論WF | オーケストレーション | 両方 | 標準 | 不可逆な副作用 |
| [P18](orchestration/p18-hitl-approval-gate.md) | HITL承認ゲート | オーケストレーション | 両方 | 標準 | 高リスク操作 |
| [P20](determinism/p20-dual-track-verification.md) | 二重トラック検証 | 確率→決定論 | 両方 | 高度 | 数値/事実/引用が重要 |
| [P21](determinism/p21-confidence-gated-abstention.md) | 信頼度ゲート棄権 | 確率→決定論 | 両方 | 標準 | 誤答コストが高い |
| [P22](reliability/p22-async-job-callback.md) | 非同期ジョブ＋コールバック | 信頼性/運用 | 両方 | 基盤 | 処理が数十秒超 |
| [P23](reliability/p23-circuit-breaker-fallback.md) | サーキットブレーカ/フォールバック | 信頼性/運用 | 両方 | 標準 | 上流LLMの可用性変動 |
| [P24](reliability/p24-semantic-cache.md) | セマンティック/プロンプトキャッシュ | 信頼性/運用 | 両方 | 標準 | 定型質問の繰り返し |
| [P25](reliability/p25-observability-tracing.md) | オブザーバビリティ/トレース | 信頼性/運用 | 両方 | 基盤 | 本番運用すべて |
| [P26](reliability/p26-eval-gate-canary.md) | 評価ゲート/カナリア | 信頼性/運用 | 両方 | 標準 | モデル/プロンプト変更 |
| [P27](reliability/p27-cost-governance.md) | コストガバナンス | 信頼性/運用 | 両方 | 標準 | コスト按分・暴走防止 |
| [P31](freshness/p31-cdc-freshness.md) | CDC駆動の知識鮮度 | 知識鮮度 | 両方 | 標準 | 頻繁に更新される知識 |
| [P33](organization/p33-department-scoped-agent.md) | 部署スコープのエージェント | 組織 | 従業員 | 標準 | 部署で業務/規制が異なる |
| [P35](organization/p35-agent-registry.md) | エージェント・レジストリ | 組織 | 両方 | 標準 | エージェントが乱立し始める |
| [P36](governance/p36-digital-employee-lifecycle.md) | デジタル従業員ライフサイクル | ガバナンス | 両方 | 標準 | エージェント増殖・統制必要 |
| [P37](governance/p37-prompt-supply-chain.md) | プロンプト・サプライチェーン | ガバナンス | 両方 | 標準 | 本番運用・複数人開発 |
| [P40](regulation/p40-feedback-flywheel.md) | フィードバックループ | 規制/改善 | 両方 | 標準 | 継続運用・品質改善 |
