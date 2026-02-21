import os
import glob
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DOCS_DIR = "/app/docs"
FAISS_PATH = "/app/faiss_data"

def load_documents():
    docs = []
    # 対応する拡張子（テキストベース）
    for ext in ("*.txt", "*.md", "*.csv"):
        for filepath in glob.glob(os.path.join(DOCS_DIR, "**", ext), recursive=True):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                filename = os.path.basename(filepath)
                # ファイル名をメタデータとして保存（RAGエンジンが出典として使用します）
                docs.append(Document(page_content=text, metadata={"source": filename}))
                print(f"読み込み成功: {filename}")
            except Exception as e:
                print(f"ファイルの読み込みに失敗しました ({filepath}): {e}")
    return docs

def create_database():
    print("=== RAG用ベクトルデータベース作成ツール ===")
    print(f"ドキュメントフォルダ: {DOCS_DIR} をスキャンしています...")
    
    docs = load_documents()
    if not docs:
        print(f"\nエラー: 読み込めるドキュメントがありません。")
        print(f"ホストの `docs/` フォルダに `.txt`, `.md`, `.csv` ファイルを配置してください。")
        return

    print(f"\n合計 {len(docs)} 個のファイルを読み込みました。テキストを分割(チャンク化)します...")
    # LLMが扱いやすいサイズにテキストを分割
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(docs)

    print(f"合計 {len(split_docs)} 個のテキストチャンクを作成しました。")
    print("\n埋め込み(Embeddings)モデルをロードし、ベクトルデータベースを構築中...")
    print("（※初回はモデルのダウンロードが発生するため時間がかかります）")
    
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    
    # FAISSインデックスの作成
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    
    # 保存
    os.makedirs(FAISS_PATH, exist_ok=True)
    vectorstore.save_local(FAISS_PATH)
    
    print(f"\n✅ データベースの更新が正常に完了しました！")
    print(f"保存先: {FAISS_PATH}")
    print("チャット画面から更新された情報に基づいて質問ができるようになりました。")

if __name__ == "__main__":
    create_database()
