from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from .loader import load_documents_from_folder

import os

DB_PATH = "backend/rag/faiss_index"

def build_vectorstore():
    """
    Load documents, embed them, and store in FAISS DB.
    """
    docs = load_documents_from_folder("backend/data/health_docs")

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(DB_PATH)

    print("Vectorstore built and saved!")


def load_vectorstore():
    """
    Load FAISS vectorstore from disk.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)