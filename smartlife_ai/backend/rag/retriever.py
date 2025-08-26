from langchain.tools.retriever import create_retriever_tool
from .vector_store import load_vectorstore

retriever = load_vectorstore()

rag_tool = create_retriever_tool(
    retriever=retriever,
    name="knowledge_search",
    description="Search expert documents about health, budget nutrition, Indian diet etc."
)