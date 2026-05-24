---
title: "設計原則"
description: "エンタープライズAIエージェント・アーキテクチャの12箇条の設計原則。"
status: done
---

# 設計原則

エンタープライズ AI エージェントのアーキテクチャを貫く12箇条の設計原則を示す。

## 原則一覧

### 1. エージェントは本人の権限を超えない

実効権限は「能力 ∩ 本人権限 ∩ ポリシー」の最小。便利さのための全権化を禁ずる。

参照：[ID-4 Permission Mirror](../patterns/id-identity/id4-permission-mirror-least-of.md) / [ID-2 OBO](../patterns/id-identity/id2-identity-federation-obo.md)

### 2. 従業員面と顧客面を物理的に分ける

最重大の事故クラス——顧客向けが社内データに到達する（逆も）——を構造的に排除する。

参照：[ID-1 二面分離](../patterns/id-identity/id1-workforce-customer-split.md)

### 3. 作らず、寄り添う

SoR を置き換えず、読み、正規手続きで書く。既存統合資産を再利用する。

参照：[RT-6 SoR Write Boundary](../patterns/rt-runtime/rt6-sor-write-boundary.md) / [IN-4 iPaaS Reuse](../patterns/in-integration/in4-existing-ipaas-reuse.md)

### 4. データはコピーする前に疑う

no-copy・JIT・ACL 同梱を既定にし、集約は目的が明確なときだけ。

参照：[KM-2 Context Mesh](../patterns/km-knowledge/km2-context-mesh.md) / [KM-1 Access-Controlled RAG](../patterns/km-knowledge/km1-access-controlled-rag.md)

### 5. 組織グラフを唯一の権威に

スコープ・共有・承認・委譲を組織構造から一貫して導く。

参照：[KM-3 Canonical Object & KG](../patterns/km-knowledge/km3-canonical-object-knowledge-graph.md) / [KM-4 Scoped Memory](../patterns/km-knowledge/km4-scoped-memory-hierarchy.md)

### 6. プロンプトでなく、アイデンティティとポリシーで守る

安全保証は実行基盤側に置く。プロンプトはセキュリティ境界にならない。

参照：[ID-7 Policy-as-Code](../patterns/id-identity/id7-policy-as-code-guardrail.md) / [ID-6 Zero-Trust](../patterns/id-identity/id6-zero-trust-pdp-pep.md)

### 7. すべての行為を三者で帰責する

人＋エージェント＋システムを相関 ID で貫き企業横断で監査する。

参照：[OB-2 Unified Audit](../patterns/ob-observability/ob2-unified-audit-lineage.md) / [OB-1 Observability Lake](../patterns/ob-observability/ob1-observability-lake.md)

### 8. 中央はガードレールと舗装路を、部署は業務ロジックを

集権と分権の二層統治。中央がインフラ・認可・監査・評価を、部署がドメイン知識・ユースケースを持つ。

参照：[GV-3 Department Factory](../patterns/gv-governance/gv3-department-agent-factory.md) / [GV-1 Control Plane](../patterns/gv-governance/gv1-agent-control-plane.md)

### 9. 自然言語はUIであり内部プロトコルではない

作用は必ず構造化コマンドへ変換する。自然言語のまま API に渡さない。

参照：[RT-5 Command Envelope](../patterns/rt-runtime/rt5-command-envelope.md) / [IN-2 SaaS Adapter](../patterns/in-integration/in2-saas-connector-adapter.md)

### 10. エージェントは「業務キューを処理する管理されたデジタル業務主体」

チャットボットではなく、登録・監査・権限制御・評価され続ける実行主体として設計する。

参照：[RT-9 Work Queue](../patterns/rt-runtime/rt9-work-queue-agent.md) / [GV-1 Control Plane](../patterns/gv-governance/gv1-agent-control-plane.md)

### 11. AIを賢くするより、企業の境界内で安全に働けるようにする

知能は前提、勝負は権限・統合・統治。

参照：[EX-1 Gateway](../patterns/ex-experience/ex1-enterprise-agent-gateway.md) / [ID-6 Zero-Trust](../patterns/id-identity/id6-zero-trust-pdp-pep.md)

### 12. やるか/やらないかでなく、どの程度かを設計する

自律度・ログ・予算・キャッシュ等の連続量を、トレースと eval で継続調整する。

参照：[「程度」の選定基準](../selection/degree-criteria.md) / [GV-7 Eval Pipeline](../patterns/gv-governance/gv7-evaluation-governance-pipeline.md)

---

> 最も凝縮すると——**AIエージェントを企業に導入するとは、LLMを業務システムにつなぐことではなく、企業のID・権限・責任・データ・プロセス・監査・組織構造の中に、新しい実行主体を安全に参加させることである。** 確率的な知能を、決定論的な権限・組織・監査の檻の中に閉じ込めたとき、初めて数万人規模の本番に耐えるエンタープライズAIエージェントが成立する。
