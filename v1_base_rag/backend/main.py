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

from backend.expense_manager import (
    initialize_expense_file,
    add_expense,
    get_all_expenses,
    get_monthly_total
)

initialize_expense_file()

class ExpenseInput(BaseModel):
    amount: float
    category: str
    note: str = ""

@app.post("/expense/add")
def add_expense_api(data: ExpenseInput):
    """
    Add a new expense with amount, category, and optional note.
    """
    return {"expense": add_expense(data.amount, data.category, data.note)}

@app.get("/expense/all")
def list_expenses_api():
    """
    Return all expenses stored in the file.
    """
    return {"expenses": get_all_expenses()}

@app.get("/expense/monthly-total")
def monthly_total_api():
    """
    Return the total amount spent this month.
    """
    return {"monthly_total": get_monthly_total()}



from backend.meal_planner import generate_meal_plan


class MealRequest(BaseModel):
    age: int
    weight: float
    height: float
    location: str
    budget: float
    diet_type: str        
    provider: str = "OpenAI"  

@app.post("/meal/plan")
def meal_plan_api(data: MealRequest):
    """
    Generate a personalized meal plan based on user input
    """
    meal_plan = generate_meal_plan(
        age=data.age,
        weight=data.weight,
        height=data.height,
        location=data.location,
        budget=data.budget,
        diet_type=data.diet_type,
        provider=data.provider
    )
    return {"meal_plan": meal_plan}