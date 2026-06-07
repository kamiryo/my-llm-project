# my-llm-project/openwebui/Dockerfile
FROM ghcr.io/open-webui/open-webui:v0.9.6

# viをインストール
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*

# 事前にHuggingFaceモデルをダウンロードしてDockerイメージ内にキャッシュする
ENV HF_HOME=/app/backend/data/cache/embedding/models
ENV SENTENCE_TRANSFORMERS_HOME=/app/backend/data/cache/embedding/models
RUN pip install sentence-transformers && \
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); SentenceTransformer('TaylorAI/bge-micro-v2')" || true

EXPOSE 8080