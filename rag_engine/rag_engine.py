# rag_engine/rag_engine.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class RAGEngine:
    def __init__(self, faiss_path: str):
        self.embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
        self.vectorstore = FAISS.load_local(
            faiss_path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )

    def search(self, query: str, k: int = 3, filter_metadata: dict = None) -> list:
        if filter_metadata:
            return self.vectorstore.similarity_search(query, k=k, filter=filter_metadata)
        else:
            return self.vectorstore.similarity_search(query, k=k)

    def build_prompt(self, query: str, docs: list[Document], use_metadata: bool = False) -> str:
        retrieved_texts = []
        for doc in docs:
            if use_metadata:
                source = doc.metadata.get("source", "出典不明")
                retrieved_texts.append(f"{doc.page_content}\n（出典: {source}）")
            else:
                retrieved_texts.append(doc.page_content)

        knowledge = "\n---\n".join(retrieved_texts)
        prompt = f"あなたは社内規則に詳しいAIアシスタントです。以下の情報を参考にして質問に答えてください。\n\n{knowledge}\n\n質問: {query}\n回答: "
        return prompt
