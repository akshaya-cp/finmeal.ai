# backend/build_index.py

# This script builds the vector store from docs (PDF/CSV/TXT) into FAISS
from rag.vector_store import build_vectorstore

if __name__ == "__main__":
    print("📚 Building FAISS vector store from health_docs...")
    build_vectorstore()
    print("✅ Vectorstore built and saved to backend/rag/faiss_index/")