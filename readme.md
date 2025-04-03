# my-llm-project

このプロジェクトは、LLM（大規模言語モデル）を使用したチャットアプリケーションのデモを目的としています。

## ディレクトリ構造

- `docker-compose.yml`: Docker Composeの設定ファイル
- `ollama/`: Ollama関連のファイル
  - `entrypoint.sh`: エントリーポイントスクリプト
  - `Dockerfile`: Dockerイメージの設定ファイル
  - `Modelfile`: モデル設定ファイル
  - `models/`: モデル関連のディレクトリ
- `openwebui/`: OpenWebUI関連のファイル
  - `Dockerfile`: Dockerイメージの設定ファイル

## 使用方法

1. Docker/Dcoker Composeをインストールしてあることをが前提です
2. GPU利用を前提に構築されています(nonGPUモデルの場合は変更が必要です)
3. `docker-compose up` コマンドを実行して、サービスを起動します。

## 注意事項

- `ollama/models/` 配下のモデルファイルはGit管理から除外しています。
- RAG用のナレッジは以下の適当なデータを格納してあります。

```
texts = [
    "育児休暇制度：最長1年間の取得が可能です。",
    "フレックス制度：10:00〜15:00をコアタイムとします。",
    "育児休暇：最長4年間取得可能。年に1回更新のための面談が必要。",
    "フレックスタイム：基本9:45〜14:30をコアとしています。"
]
metadatas = [
    {"company": "A", "source": "https://intra.a社.jp/rules育休"},
    {"company": "A", "source": "https://intra.a社.jp/rulesフレックス"},
    {"company": "B", "source": "https://intra.b社.jp/rules育休"},
    {"company": "B", "source": "https://intra.b社.jp/rulesフレックス"}
]
```