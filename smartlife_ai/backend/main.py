from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SmartLife AI Backend",
    description="Backend for expense + meal planner",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message" : "Welcome to SmartLife AI Backend! Let's hit it off",
        "status" : "Running",
    }

@app.get("/health")
def health_check():
    return {
        "status" : "OK",
        "service" : "backend",
        "version" : "1.0.0"
    }

from pydantic import BaseModel
from typing import List
from backend.ai_agent import get_response_from_ai_agent

class RequestState(BaseModel):
    model_name : str
    model_provider : str
    system_prompt : str
    messages : List[str]
    allow_search : bool

@app.post("/chat")
def chat_endpoint(request : RequestState):
    """
    Main API Endpoint to talk with the LangGraph-powered AI agent
    """
    ALLOWED_MODEL_NAMES = ["deepseek-r1-distill-llama-70b", "gpt-4o", "gpt-4o-mini"]

    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model."}

    response = get_response_from_ai_agent(
        llm_id=request.model_name,
        query=request.messages,
        allow_search=request.allow_search,
        system_prompt=request.system_prompt,
        provider=request.model_provider
    )

    return {"response" : response}