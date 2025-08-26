import streamlit as st
import requests

API_URL = "http://127.0.0.1:8080"

st.set_page_config(page_title="SmartLife AI", layout="centered")
st.title("SmartLife AI: Expense + Meal Planner")

tab1, tab2, tab3 = st.tabs(["Expense Tracker", "Meal Planner", "Ask AI"])

with tab1:
    st.header("💰 Track Your Daily Expenses")

    with st.form("add_expense_form"):
        amount = st.number_input("Amount Spent (₹)", min_value=1.0)
        category = st.selectbox("Category", ["Groceries", "Transport", "Food", "Entertainment", "Other"])
        note = st.text_input("Note (optional)")
        submitted = st.form_submit_button("➕ Add Expense")

        if submitted:
            payload = {"amount": amount, "category": category, "note": note}
            res = requests.post(f"{API_URL}/expense/add", json=payload)

            if res.status_code == 200:
                st.success("Expense added successfully!")
    
    
    st.subheader("📊 Monthly Total")
    res = requests.get(f"{API_URL}/expense/monthly-total")
    if res.status_code == 200:
        st.info(f"Total spent this month: ₹{res.json()['monthly_total']}")

    
    st.subheader("📋 All Expenses")
    res = requests.get(f"{API_URL}/expense/all")
    if res.status_code == 200:
        for exp in reversed(res.json()["expenses"]):
            st.markdown(f"- ₹{exp['amount']} on **{exp['category']}** — _{exp['note']}_ at `{exp['date']}`")



with tab2:
    st.header("🥗 Personalized Meal Plan Generator")

    with st.form("meal_form"):
        age = st.number_input("Age", min_value=10, max_value=100)
        weight = st.number_input("Weight (kg)", min_value=30.0)
        height = st.number_input("Height (cm)", min_value=100.0)
        location = st.text_input("Your Location (e.g., Kanpur, Delhi)")
        budget = st.number_input("Daily Food Budget (₹)", min_value=20.0)
        diet_type = st.radio("Diet Type", ["Veg", "Non-Veg"])
        provider = st.selectbox("LLM Provider", ["OpenAI", "Groq"])
        meal_btn = st.form_submit_button("🍽️ Generate Meal Plan")

        if meal_btn:
            meal_payload = {
                "age": age,
                "weight": weight,
                "height": height,
                "location": location,
                "budget": budget,
                "diet_type": diet_type,
                "provider": provider
            }
            res = requests.post(f"{API_URL}/meal/plan", json=meal_payload)
            if res.status_code == 200:
                st.subheader("🍱 Recommended Meal Plan")
                st.markdown(res.json()["meal_plan"])
            else:
                st.error("Failed to get meal plan.")



with tab3:
    st.header("🧠 Ask SmartLife AI")

    system_prompt = st.text_area("Set Assistant Behavior", "Act as a helpful finance and health advisor")

    provider = st.radio("Model Provider", ("OpenAI", "Groq"))
    model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"] if provider == "OpenAI" else ["deepseek-r1-distill-llama-70b"])

    allow_search = st.checkbox("Enable Web Search")

    query = st.text_area("Your Question", placeholder="e.g., What's the best ₹50 protein meal for vegetarians?")

    if st.button("🚀 Ask Agent"):
        if query.strip():
            payload = {
                "model_name": model,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [query],
                "allow_search": allow_search
            }
            res = requests.post(f"{API_URL}/chat", json=payload)
            if res.status_code == 200:
                if "error" in res.json():
                    st.error(res.json()["error"])
                else:
                    st.success("✅ AI Response")
                    st.markdown(res.json()["response"])
            else:
                st.error("Something went wrong with the agent.")