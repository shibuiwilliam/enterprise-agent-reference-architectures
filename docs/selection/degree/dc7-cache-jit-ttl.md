---
title: "DC-7 キャッシュ積極度・JIT 資格情報 TTL"
description: "検索キャッシュとJIT資格情報のTTLを用途リスクに応じて調整する連続量パラメータ。"
status: done
---

# DC-7 キャッシュ積極度・JIT 資格情報 TTL

## 概要

同じ質問を 10 人が連続で投げたとき、毎回フル推論するのはコストの無駄だ。一方、人事異動の直後に「この人の部下一覧」をキャッシュから返せば、古い組織図に基づく誤った結果を返してしまう。同様に、JIT で発行した一時認証トークン（[ID-5](../../patterns/id-identity/id5-jit-scoped-credentials.md)）の有効期間を長くすれば再認証の手間は減るが、権限剥奪後もアクセスが残るリスクが生まれる。キャッシュの積極度と資格情報の TTL を、用途のリスクに応じて調整する方法を扱う。

<!-- machine-readable decision rules for coding agents -->
```yaml
id: DC-7
parameter: cache_jit_ttl
rules:
  - condition: "data_freshness_requirement == 'tolerate_stale' AND operation_risk == 'low' AND personalized == false"
    cache_strategy: aggressive
    cache_ttl: long
    jit_credential_ttl: hours
    reason: "変化が少なく非パーソナライズかつ低リスクなデータは積極的にキャッシュしてレイテンシとコストを削減できる"
  - condition: "data_freshness_requirement == 'real_time' OR personalized == true OR data_classification IN ['department_confidential', 'top_secret']"
    cache_strategy: disabled
    jit_credential_ttl: minutes
    reason: "パーソナライズ応答・時系列依存データ・機密情報を含む取得結果はキャッシュを無効化し、常にフレッシュな取得を行う"
  - condition: "operation_has_side_effects == true OR confidential_data_in_result == true"
    cache_strategy: disabled
    similarity_threshold: high
    reason: "高害リスク領域（機密情報を含む検索・副作用を持つ操作）は類似度閾値を高く設定し、TTLを短くする"
  - condition: "permission_change_event == true"
    action: force_expire_jit_credentials
    reason: "権限変更・退職・セッション終了を検知してTTL期限前に資格情報を強制失効させる仕組みを設ける"
  - condition: "data_freshness_requirement != 'real_time' AND operation_has_side_effects == false"
    action: invalidate_cache_on_permission_event
    reason: "キャッシュが古い権限状態を保持するとID-4で実現した最小権限の効果が損なわれる。キャッシュ無効化と権限変更イベントを連動させる"
```

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（消極的すぎ・TTL 短すぎ） | キャッシュなし、資格情報が即時失効 | 毎回検索・認証が発生しレイテンシが増大する。JIT 資格情報の再発行コストが高い処理では詰まりが生じる |
| 過大（積極的すぎ・TTL 長すぎ） | キャッシュを広く長く保持 | 古い検索結果を使い続ける。退職・権限変更後も JIT 資格情報が有効なまま残留し、権限超過リスクが生じる |

## 判断基準

キャッシュと資格情報 TTL は、用途のリスク特性に応じて個別に設定する。

**検索キャッシュ**

- 完全一致キャッシュをプライマリ、セマンティックキャッシュをセカンダリとして使う
- 高リスク領域（機密情報を含む検索・副作用を伴う操作）は類似度閾値を高く設定し、TTL は短くする
- パーソナライズ応答・時系列依存データ・機密情報を含む取得結果はキャッシュを無効化し、常にフレッシュな取得を行う

**JIT 資格情報 TTL**

- [ID-5](../../patterns/id-identity/id5-jit-scoped-credentials.md) の用途リスクで TTL を分ける。機密データアクセスや副作用を伴う操作は分単位の短い TTL、参照のみの軽量操作は時間単位の相対的に長い TTL とする
- 権限変更・退職・セッション終了を検知したら、TTL 期限前に資格情報を強制失効させる仕組みを設けておく

!!! tip "キャッシュと最小権限の整合"
    キャッシュが古い権限状態を保持すると、[ID-4 Permission Mirror & Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md) で実現した最小権限の効果が損なわれる。キャッシュ無効化と権限変更イベントを連動させること。

## 調整の仕組み

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でキャッシュヒット率・ミス率・TTL 期限切れ発生率を計測する
- ヒット率が低い経路では TTL 延長や類似度閾値の緩和を検討する。逆にヒット率が高い経路でも、コンテンツの鮮度要件を定期的に確認する
- JIT 資格情報の残留を検出したらアラートを発し、失効処理を自動実行できる仕組みを整える

## 関連パターン

- [ID-5 JIT Scoped Credentials](../../patterns/id-identity/id5-jit-scoped-credentials.md) — 一時資格情報の発行・失効の本体
- [ID-4 Permission Mirror & Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md) — 最小権限との整合
- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — 権限認識 RAG でのキャッシュ設計
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — フェデレーテッド取得のキャッシュ層
