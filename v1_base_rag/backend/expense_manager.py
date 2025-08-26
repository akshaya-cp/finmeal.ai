import json
from datetime import datetime
from typing import List, Dict

EXPENSE_FILE = "backend/data/expenses.json"

def initialize_expense_file():
    import os
    os.makedirs("backend/data", exist_ok=True)
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w") as f:
            json.dump([], f) 

def add_expense(amount: float, category: str, note: str = "") -> Dict:
    """
    Adds a new expense to the expenses.json file.
    """
    new_expense = {
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(EXPENSE_FILE, "r") as f:
        expenses = json.load(f)

    expenses.append(new_expense)

    with open(EXPENSE_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

    return new_expense

def get_all_expenses() -> List[Dict]:
    """
    Returns the list of all expenses stored.
    """
    with open(EXPENSE_FILE, "r") as f:
        expenses = json.load(f)
    return expenses

def get_monthly_total() -> float:
    """
    Calculates total expenses for the current month.
    """
    now = datetime.now()
    current_month = now.strftime("%Y-%m")

    with open(EXPENSE_FILE, "r") as f:
        expenses = json.load(f)

    monthly_total = sum(
        item["amount"]
        for item in expenses
        if item["date"].startswith(current_month)
    )

    return round(monthly_total, 2)