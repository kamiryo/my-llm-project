# my-llm-project

このプロジェクトは、LLM（大規模言語モデル）を使用したチャットアプリケーションと、RAG（Retrieval Augmented Generation）機能を組み合わせたシステムを構築することを目的としています。

## 概要

このプロジェクトは以下の3つの主要コンポーネントで構成されています：

1. **Ollama**: ローカルで動作するLLMサーバー（DeepSeek R1 Distill Qwen 14B 日本語モデルを使用）
2. **Open WebUI**: OllamaのWebインターフェース
3. **RAG Engine**: 文書検索と生成を組み合わせたシステム

## ディレクトリ構造

- `docker-compose.yml`: Docker Composeの設定ファイル
- `ollama/`: Ollama関連のファイル
  - `Dockerfile`: Ollamaのカスタムイメージ設定
  - `Modelfile`: DeepSeek日本語モデルの設定
  - `entrypoint.sh`: コンテナ起動時の初期化スクリプト
  - `models/`: モデルファイル配置用ディレクトリ（*.gguf）
- `openwebui/`: Open WebUI関連のファイル
  - `Dockerfile`: Open WebUIのカスタムイメージ設定
- `rag_engine/`: RAG機能を提供するFastAPIサーバー
  - `app.py`: メインアプリケーション（FastAPI）
  - `rag_engine.py`: RAG機能の中核ロジック
  - `requirements.txt`: 依存パッケージリスト
  - `Dockerfile`: RAGエンジンのイメージ設定
- `faiss_data/`: FAISSベクトルデータベース保存用ディレクトリ（.gitignore対象）

## 前提条件

- Docker と Docker Compose がインストールされていること
- NVIDIA GPU と適切なドライバーがインストールされていること
- Docker の NVIDIA Container Toolkit が設定されていること

## 使用方法

1. モデルファイルを取得し、`ollama/models/` ディレクトリに配置します：
   - `cyberagent-DeepSeek-R1-Distill-Qwen-14B-Japanese-Q4_K_M.gguf`

2. Docker Compose でサービスを起動します：
   ```bash
   docker-compose up -d
   ```

3. 以下のサービスにアクセスできます：
   - Open WebUI: http://localhost:3000
   - RAG API: http://localhost:5001
   - Ollama API: http://localhost:11434

## RAG機能について

RAG Engineは、FAISSベクトルデータベースを使用して効率的な検索を行い、以下の特徴を持っています：

- 日本語の検索クエリに対応（multilingual-e5-large埋め込みモデル使用）
- メタデータによるフィルタリング機能
- OpenAI互換APIの提供

サンプルのRAGナレッジベース(faiss_data)には以下のようなデータが含まれています：

```python
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

## 注意事項

- モデルファイル（*.gguf）とベクトルデータベース（faiss_data/）はGit管理対象外です
- GPUを使用しない環境では、`docker-compose.yml`の`deploy`セクションを修正してください
