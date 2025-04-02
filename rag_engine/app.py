# rag_engine/app.py
# from flask import Flask, request, jsonify
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rag_engine import RAGEngine
import os
import requests
import uvicorn
import json

#app = Flask(__name__)
app = FastAPI()

# 環境変数 or デフォルトからパス指定
VECTOR_DB_PATH = os.environ.get("VECTOR_DB_PATH", "faiss_data/faiss_index_colab")
rag = RAGEngine(faiss_path=VECTOR_DB_PATH)

@app.post("/rag")
async def chat_with_rag(request: Request):
    try:
        body = await request.json()  # JSONデコード試行
    except Exception as e:
        # ログ出力してエラーをクライアントに返す
        print("📛 JSON decode error:", e)
        return JSONResponse(
            content={"error": "Invalid JSON or encoding", "detail": str(e)},
            status_code=400
        )

    query = body.get("query", "")
    use_metadata = body.get("use_metadata", False)
    filter_metadata = body.get("filter", None)

    docs = rag.search(query=query, k=3, filter_metadata=filter_metadata)
    prompt = rag.build_prompt(query=query, docs=docs, use_metadata=use_metadata)

    return JSONResponse(content={"prompt": prompt})

@app.get("/v1/models")
async def get_models(request: Request):
    return JSONResponse(content={
        "object": "list",
        "data": [
            {
                "id": "my-local-model",
                "object": "model",
                "created": 1711910400,
                "owned_by": "local-user"
            }
        ]
    })

@app.post("/v1/chat/completions")
async def chat_with_rag(request: Request):
    body = await request.json()
    query = body["messages"][-1]["content"]  # ユーザーの最新質問を取得
    use_metadata = body.get("use_metadata", True)

    # ベクトル検索
    docs = rag.search(query=query, k=3)
    # プロンプト構築
    prompt = rag.build_prompt(query=query, docs=docs, use_metadata=use_metadata)

    # Ollamaへプロンプトを渡して生成（ストリーミング対応）
    response = requests.post(
        "http://ollama-gpu:11434/api/generate",
        json={"model": "my-deepseek-model:latest", "prompt": prompt},
        stream=True  # ストリームとして受信
    )

    # ストリーミングレスポンスからレスポンス本文を構築
    response_text = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            try:
                data = json.loads(line)
                response_text += data.get("response", "")
            except json.JSONDecodeError as e:
                print(f"[JSON decode error] {e} in line: {line}")

    if not response_text.strip():
        raise ValueError(f"Ollamaから期待する形式で結果が返ってきませんでした: {response.text}")

    # OpenAI互換のレスポンス形式で返す
    return {
        "id": "chatcmpl-rag001",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": response_text},
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
