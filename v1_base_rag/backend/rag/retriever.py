# from langchain.tools.retriever import create_retriever_tool
# from .vector_store import load_vectorstore
from langchain_core.tools import tool
from backend.rag.vector_store import get_vectorstore
# from backend.rag.vector_store import load_vectorstore


# retriever = load_vectorstore()
retriever = get_vectorstore().as_retriever()
@tool
def rag_tool(query: str) -> str:
    """Searches the health document vector store and returns relevant context."""
    docs = retriever.get_relevant_documents(query)
    return "\n\n".join([doc.page_content for doc in docs])

# rag_tool = create_retriever_tool(
#     retriever=retriever,
#     name="knowledge_search",
#     description="Search expert documents about health, budget nutrition, Indian diet etc."
# )