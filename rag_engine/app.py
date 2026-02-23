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
VECTOR_DB_PATH = os.environ.get("VECTOR_DB_PATH", "faiss_data")
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

from fastapi.responses import JSONResponse, StreamingResponse

@app.post("/v1/chat/completions")
async def chat_with_rag(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    stream = body.get("stream", False)
    use_metadata = body.get("use_metadata", True)

    if not messages:
        return JSONResponse(content={"error": "messages required"}, status_code=400)

    # 最新のユーザー発言のみで検索
    query = messages[-1]["content"]
    docs = rag.search(query=query, k=3)
    context = rag.build_prompt(query=query, docs=docs, use_metadata=use_metadata)

    # 会話履歴をフォーマット
    chat_history = ""
    for message in messages[:-1]:
        role = message.get("role", "")
        content = message.get("content", "")
        if role == "user":
            chat_history += f"ユーザー: {content}\n"
        elif role == "assistant":
            chat_history += f"アシスタント: {content}\n"

    # 履歴と検索結果を統合したプロンプトを作成
    prompt = f"{chat_history}\n---\n以下は知識ベースの情報です。\n{context}\n\n質問: {query}\n回答: "
    print(f"🚄 LLMエンジン行きのプロンプトは以下の通りです---\n{prompt}")

    if stream:
        async def event_stream():
            response = requests.post(
                "http://ollama-gpu:11434/api/generate",
                json={"model": "my-nemotron-model:latest", "prompt": prompt},
                stream=True
            )
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        chunk_text = data.get("response", "")
                        
                        chunk = {
                            "id": "chatcmpl-rag001",
                            "object": "chat.completion.chunk",
                            "choices": [{
                                "index": 0, 
                                "delta": {"content": chunk_text}, 
                                "finish_reason": None
                            }]
                        }
                        yield f"data: {json.dumps(chunk)}\n\n"
                    except json.JSONDecodeError:
                        pass
            
            # 完了シグナル
            final_chunk = {
                "id": "chatcmpl-rag001",
                "object": "chat.completion.chunk",
                "choices": [{
                    "index": 0, 
                    "delta": {}, 
                    "finish_reason": "stop"
                }]
            }
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"
            
        return StreamingResponse(event_stream(), media_type="text/event-stream")

    else:
        # Ollamaへプロンプトを渡して生成（ストリーミングなしの通常応答）
        response = requests.post(
            "http://ollama-gpu:11434/api/generate",
            json={"model": "my-nemotron-model:latest", "prompt": prompt},
            stream=True
        )

        response_text = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    data = json.loads(line)
                    response_text += data.get("response", "")
                except json.JSONDecodeError as e:
                    pass

        if not response_text.strip():
            raise ValueError(f"Ollamaから期待する形式で結果が返ってきませんでした: {response.text}")

        return JSONResponse(content={
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
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
