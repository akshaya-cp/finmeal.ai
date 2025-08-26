from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import os

def load_documents_from_folder(folder_path: str) -> List[str]:
    """
    Loads all supported documents from the given folder and splits them into chunks.
    Supported formats: .pdf, .csv, .txt
    """
    docs = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".csv"):
            loader = CSVLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            continue

        raw_docs = loader.load()
        docs.extend(raw_docs)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    return split_docs