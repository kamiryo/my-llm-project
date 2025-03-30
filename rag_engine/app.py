# rag_engine/app.py
from flask import Flask, request, jsonify
from rag_engine import RAGEngine

app = Flask(__name__)
rag = RAGEngine(faiss_path="faiss_data/faiss_index_colab")

@app.route("/rag", methods=["POST"])
def rag_search():
    data = request.get_json()
    query = data.get("query")
    filter_metadata = data.get("filter")
    use_metadata = data.get("use_metadata", False)

    docs = rag.search(query, filter_metadata=filter_metadata)
    prompt = rag.build_prompt(query, docs, use_metadata=use_metadata)
    return jsonify({"prompt": prompt})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
