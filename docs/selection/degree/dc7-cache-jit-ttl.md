---
title: "DC-7 キャッシュ積極度・JIT 資格情報 TTL"
description: "検索キャッシュとJIT資格情報のTTLを用途リスクに応じて調整する連続量パラメータ。"
status: done
---

# DC-7 キャッシュ積極度・JIT 資格情報 TTL

## 概要

同じ質問を 10 人が連続で投げたとき、毎回フル推論するのはコストの無駄である。しかし人事異動の直後に「この人の部下一覧」をキャッシュから返せば、古い組織図に基づく誤った結果になる。同様に、JIT で発行した一時認証トークン（[ID-5](../../patterns/id-identity/id5-jit-scoped-credentials.md)）の有効期間を長くすれば再認証の手間は減るが、権限剥奪後もアクセスが残るリスクが生まれる。キャッシュの積極度と資格情報の TTL を、用途のリスクに応じてどう調整するかを扱う。

## 過小・過大の害

| 極 | 状態 | 害 |
|---|---|---|
| 過小（消極的すぎ・TTL 短すぎ） | キャッシュなし、資格情報が即時失効 | 毎回検索・認証が発生しレイテンシが増大する。JIT 資格情報の再発行コストが高い処理では詰まりが生じる |
| 過大（積極的すぎ・TTL 長すぎ） | キャッシュを広く長く保持 | 古い検索結果を使い続ける。退職・権限変更後も JIT 資格情報が有効なまま残留し、権限超過リスクが生じる |

## 判断基準

キャッシュと資格情報 TTL は、用途のリスク特性に応じて個別に設定する。

**検索キャッシュ**

- 完全一致キャッシュをプライマリ、セマンティックキャッシュをセカンダリとして利用する
- 高害リスク領域（機密情報を含む検索・副作用を持つ操作）は類似度閾値を高く設定し、TTL を短くする
- パーソナライズ応答・時系列依存データ・機密情報を含む取得結果はキャッシュを無効化し、常にフレッシュな取得を行う

**JIT 資格情報 TTL**

- [ID-5](../../patterns/id-identity/id5-jit-scoped-credentials.md) の用途リスクで TTL を分ける。機密データアクセスや副作用を伴う操作は短い TTL（分単位）、参照のみの軽量操作は相対的に長い TTL（時間単位）とする
- 権限変更・退職・セッション終了を検知して TTL 期限前に資格情報を強制失効させる仕組みを設ける

!!! tip "キャッシュと最小権限の整合"
    キャッシュが古い権限状態を保持すると、[ID-4 Permission Mirror & Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md) で実現した最小権限の効果が損なわれる。キャッシュ無効化と権限変更イベントを連動させる。

## 調整の仕組み

- [OB-1 Observability Lake](../../patterns/ob-observability/ob1-observability-lake.md) でキャッシュヒット率・ミス率・TTL 期限切れ発生率を計測する
- キャッシュヒット率が低い経路は TTL 延長・類似度閾値緩和を検討し、ヒット率が高い経路でもコンテンツの鮮度要件を定期確認する
- JIT 資格情報の残留を検出したらアラートを発し、失効処理を自動実行する仕組みを整える

## 関連パターン

- [ID-5 JIT Scoped Credentials](../../patterns/id-identity/id5-jit-scoped-credentials.md) — 一時資格情報の発行・失効の本体
- [ID-4 Permission Mirror & Least-of](../../patterns/id-identity/id4-permission-mirror-least-of.md) — 最小権限との整合
- [KM-1 Access-Controlled RAG](../../patterns/km-knowledge/km1-access-controlled-rag.md) — 権限認識 RAG でのキャッシュ設計
- [KM-2 Context Mesh](../../patterns/km-knowledge/km2-context-mesh.md) — フェデレーテッド取得のキャッシュ層
