# my-llm-project

このプロジェクトは、LLM（大規模言語モデル）を使用したアプリケーションの開発を目的としています。

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

1. Dockerをインストールします。
2. `docker-compose up` コマンドを実行して、サービスを起動します。

## 注意事項

- `ollama/models/` ディレクトリはGit管理から除外されています。