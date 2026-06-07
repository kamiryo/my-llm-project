# OLLAMA の公式イメージをベースにする
FROM ollama/ollama:0.30.6

# 必要なツールをインストール（デバッグ用、不要なら削除可）
RUN apt-get update && apt-get install -y curl vim && rm -rf /var/lib/apt/lists/*

# モデルファイルをコピー


# Modelfile をコピー
COPY ./Modelfile /Modelfile

# API のポートを開放
EXPOSE 11434

# エントリーポイントスクリプトをコピーして実行可能にする
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# エントリーポイントスクリプトを実行
ENTRYPOINT ["/entrypoint.sh"]