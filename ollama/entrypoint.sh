#!/bin/sh

# OLLAMAサーバーをバックグラウンドで起動
ollama serve &

# OLLAMAサーバーの起動を待機
echo "Waiting for OLLAMA server to start..."
until curl -s -f "http://localhost:11434/api/tags" > /dev/null 2>&1; do
    echo "Waiting for OLLAMA server..."
    sleep 2
done
echo "OLLAMA server is ready!"

# モデルが存在するか確認
if ! ollama list | grep -q "my-qwen-model"; then
    echo "Creating model..."
    ollama create my-qwen-model -f /Modelfile
    echo "Model created successfully!"
else
    echo "Model already exists!"
fi

# コンテナを実行し続ける
# exec tail -f /dev/null
wait