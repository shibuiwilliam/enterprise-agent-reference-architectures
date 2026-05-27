---
title: "「相反する仕組み」の選定基準"
description: "OBO vs サービスアカウント、中央レイク vs Mesh、Copilot vs Autopilot など12軸の二者択一の判断基準。"
status: done
---

# 「相反する仕組み」の選定基準

二者択一に見える対立の多くは、「どこで線を引くか」が答えだ。エンタープライズにおける決定的な12軸を以下に示す。各軸は比較表・判断基準・ハイブリッドアプローチ・関連パターンで構成し、抽象的な優劣ではなく条件付きの選択基準を提示する。

| ID | 名称 | 概要 |
|---|---|---|
| [TO-1](to1-obo-vs-service-account.md) | OBO委譲 vs サービスアカウント | 権限忠実性・監査帰責・実装コストの三軸で使い分けを決める |
| [TO-2](to2-lake-vs-mesh.md) | 中央集権データレイク vs フェデレーテッド Context Mesh | データ種別と権限管理方式でインデックス戦略を分割する |
| [TO-3](to3-single-vs-multi-agent.md) | 単一エージェント vs RACI マルチエージェント | 「複雑だから」でなく「責任分担が複数に分かれるから」がマルチ化の基準 |
| [TO-4](to4-readonly-vs-write.md) | Read-only vs Write-capable（段階的拡張） | 参照系と更新系を明確に分離し、段階的に権限を拡張する |
| [TO-5](to5-copilot-vs-autopilot.md) | Copilot vs Autopilot | 更新系APIはHitLのCopilot、参照系はAutopilotに分離する |
| [TO-6](to6-personal-vs-team-memory.md) | 個人の記憶 vs プロジェクト/チームの記憶 | 個人領域と共有領域を物理・論理的に分離し混線を防ぐ |
| [TO-7](to7-full-vs-selective-log.md) | 全プロンプトログ vs 選択的トレースログ | 三層分離でコスト・機密・再現性を両立する |
| [TO-8](to8-central-vs-federation.md) | 中央集権プラットフォーム vs 部署フェデレーション | ガードレールは中央、業務ロジックは部署が持つ二層統治 |
| [TO-9](to9-custom-vs-ipaas.md) | コネクタ自前構築 vs 既存 iPaaS 再利用 | 既存資産の認可粒度を検証し、不足分のみMCP化する |
| [TO-10](to10-onprem-vs-external.md) | 内部/オンプレモデル vs 外部 API | データ分類で推論経路を自動ルーティングする |
| [TO-11](to11-sync-vs-async.md) | 同期 vs 非同期 | 所要時間と承認フローの有無で処理方式を選択する |
| [TO-12](to12-prompt-vs-platform.md) | プロンプトで守る vs ポリシー/実行基盤で守る | セキュリティ境界は必ず実行基盤側に置く |
