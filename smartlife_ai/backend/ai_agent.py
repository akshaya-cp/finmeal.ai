import os
from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables from .env

# LLM Providers
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

# LangGraph agent + message utilities
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Search tool (Tavily) and RAG retriever
from langchain_tavily.tavily_search import TavilySearch
from backend.rag.retriever import rag_tool

# ✅ Set up available LLMs
openai_llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

groq_llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# ✅ Tavily Web Search Tool
search_tool = TavilySearch(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

# 🧠 MAIN FUNCTION TO GET AI RESPONSE
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    """
    Returns response from LangGraph-based AI agent using selected LLM provider.
    
    Parameters:
    - llm_id: selected model name
    - query: user's input string or list of messages
    - allow_search: bool, whether to allow real-time search
    - system_prompt: (currently unused)
    - provider: "Groq" or "OpenAI"
    """
    # 🔁 Choose LLM based on provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id, groq_api_key=os.getenv("GROQ_API_KEY"))
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, openai_api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError("Invalid provider")

    # 🛠️ Choose tools for the agent
    tools = [rag_tool]  # 🧠 Always include RAG (FAISS-based)
    if allow_search:
        tools.append(search_tool)  # 🌐 Add web search if enabled

    # 🤖 Create LangGraph Agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        # system_message=system_prompt (optional)
    )

    # 📩 Prepare state for agent
    state = {"messages": query}

    # 🚀 Run agent
    response = agent.invoke(state)

    # 🧾 Extract and return final AI message
    messages = response.get("messages")
    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]

    return ai_messages[-1]