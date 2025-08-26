import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

from langchain_tavily.tavily_search import TavilySearch

openai_llm = ChatOpenAI(
    model = "gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

groq_llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

search_tool = TavilySearch(
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    """
    Returns response from LangGraph-based AI agent using given model/provider
    """
    if provider == "Groq":
        llm = ChatGroq(model=llm_id, groq_api_key=os.getenv("GROQ_API_KEY"))
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, openai_api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError("Invalid provider")
    
    tools = [search_tool] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        # system_message=system_prompt 
    )

    state = {"messages": query}

    response = agent.invoke(state)

    messages = response.get("messages")
    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]
    return ai_messages[-1]  