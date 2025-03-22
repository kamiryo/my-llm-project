# my-llm-project/openwebui/Dockerfile
FROM ghcr.io/open-webui/open-webui:main

# viをインストール
RUN apt-get update && apt-get install -y vim && rm -rf /var/lib/apt/lists/*

EXPOSE 8080