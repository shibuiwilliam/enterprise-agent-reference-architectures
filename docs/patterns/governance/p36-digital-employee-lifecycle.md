---
id: P36
slug: DIGITAL-EMPLOYEE-LIFECYCLE
title: "P36 · DIGITAL-EMPLOYEE-LIFECYCLE — エージェントを「デジタル従業員」として統制"
category: ガバナンス
audience: both
maturity: 標準
related: [P35, P08, P26]
status: done
---

# P36 · DIGITAL-EMPLOYEE-LIFECYCLE — エージェントを「デジタル従業員」として統制

!!! abstract "一言で"
    エージェントを人間の従業員に準え、入社/職務記述/上司/人事考課/退職/緊急解雇のライフサイクルで統制するパターン。各エージェントに固有ID・オーナー（人間）・所属部署・職務範囲を割り当て、人間の従業員管理と同等のガバナンスを適用する。

## 解決する問題

- **野良エージェント**: 誰が作ったか分からないエージェントが本番で稼働し続ける。
- **オーナー不在**: 開発者の異動後にメンテナンスも停止判断もできない。
- **permission creep（権限漸増）**: 初期設定後に権限が追加され続け、過剰な権限を持つ状態になる。
- **停止手段の欠如**: 暴走や障害時にエージェントを即座に止める手段がない。

## 選定条件

**採用する場合（When to use）**

- エージェントが増殖する／野良エージェント・権限漸増・暴走時の停止手段の欠如が懸念される。
- エージェントが増加するすべての組織（早期導入が望ましい）。

**採用しない場合（When NOT）**

- エージェントが数個の初期段階（軽量版で十分）。

## 構造

- **入社（プロビジョニング）**: 最小権限でIDを発行し、試用期間（shadow / 低トラフィック）で稼働させる。
- **在職（運用）**: 定期eval（[P26](../reliability/p26-eval-gate-canary.md)）による人事考課・権限棚卸しを実施。
- **退職（デプロビジョニング）**: ID失効・RAG索引/メモリからの情報削除・依存先の付け替え。
- **緊急停止（kill switch）**: 個別/部署/全社フリート単位で即時停止できる仕組みを用意。
- レジストリ（[P35](../organization/p35-agent-registry.md)）と連動し、全エージェントの台帳を維持する。

## ユースケース

- 新規エージェントの「入社」時にOktaでワークロードIDを発行し、最小権限のスコープで試用期間を設定。1週間のshadow運行でeval結果が基準を満たした後に本番トラフィックを許可する。
- 四半期ごとの権限棚卸しで、不要になったSalesforce APIスコープを自動検出し、オーナーに削除を促す。

## 実装メモ

エージェントレジストリ（[P35](../organization/p35-agent-registry.md)）、ワークロードID（[P08](../identity/p08-token-exchange-obo.md)）、権限棚卸し、フリート制御プレーン、フィーチャーフラグ（kill switch）。

## 関連パターン

**カテゴリ**: ガバナンス ／ **対象**: 両方 ／ **成熟度**: 標準

- [P35 エージェント・レジストリ](../organization/p35-agent-registry.md)
- [P08 Token Exchange / OBO](../identity/p08-token-exchange-obo.md)
- [P26 Evalゲート/カナリア](../reliability/p26-eval-gate-canary.md)
