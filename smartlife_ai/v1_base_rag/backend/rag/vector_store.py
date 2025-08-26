from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
# from langchain_openai import OpenAIEmbeddings   # not using anymore (quota issue)

from langchain_community.embeddings import HuggingFaceEmbeddings

from .loader import load_documents_from_folder

import os
from dotenv import load_dotenv
load_dotenv() 

# print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")).   # not using anymore (quota issue)
DB_PATH = "backend/rag/faiss_index"

def build_vectorstore():
    """
    Load documents, embed them, and store in FAISS DB.
    """
    docs = load_documents_from_folder("backend/data/health_docs")

    # embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")).  # not using anymore (quota issue)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(DB_PATH)

    print("Vectorstore built and saved!")


def load_vectorstore():
    """
    Load FAISS vectorstore from disk.
    """
    # embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

def get_vectorstore():
    """
    Loads the FAISS vector store from disk and returns retriever.
    """
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings

    DB_PATH = "backend/rag/faiss_index"
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    return FAISS.load_local(DB_PATH, embeddings=embedding_model, allow_dangerous_deserialization=True)