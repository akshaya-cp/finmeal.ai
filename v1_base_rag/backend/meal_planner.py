import os
from dotenv import load_dotenv
load_dotenv()


from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

openai_llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

groq_llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def generate_meal_plan(age: int, weight: float, height: float, location: str,budget: float, diet_type: str, provider: str = "OpenAI") -> str:
    """
    Generates a personalized meal plan using LLM.
    Inputs: personal info + location + budget + diet preference
    Output: meal plan text
    """

    if provider == "OpenAI":
        llm = openai_llm
    elif provider == "Groq":
        llm = groq_llm
    else:
        raise ValueError("Invalid provider")
    
    prompt = f"""
    Act like a certified Indian dietitian.
    Your goal is to create a HEALTHY DAILY MEAL PLAN for the user.
    User Profile:
    - Age: {age}
    - Weight: {weight} kg
    - Height: {height} cm
    - Location: {location}
    - Budget: ₹{budget} per day
    - Diet Type: {diet_type}

    Constraints:
    - Use locally available ingredients in {location}
    - Stay under ₹{budget} for all meals combined
    - Provide 3 main meals and 2 snacks
    - Include estimated calories per meal
    - Output in bullet format

    Now, suggest the best possible meal plan:
    """

    response = llm.invoke(prompt)
    return response.content