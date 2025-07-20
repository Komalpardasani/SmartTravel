import json
import os

EXPENSES_FILE = os.path.join("data", "expenses.json")

def load_all_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return {}
    with open(EXPENSES_FILE, "r") as f:
        return json.load(f)

def load_expenses(user_email):
    all_data = load_all_expenses()
    return all_data.get(user_email, [])

def save_expense(user_email, expense):
    all_data = load_all_expenses()
    if user_email not in all_data:
        all_data[user_email] = []
    all_data[user_email].append(expense)
    with open(EXPENSES_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def clear_expenses(user_email):
    all_data = load_all_expenses()
    if user_email in all_data:
        all_data[user_email] = []
    with open(EXPENSES_FILE, "w") as f:
        json.dump(all_data, f, indent=2)
