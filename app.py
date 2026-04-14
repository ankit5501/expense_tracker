from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "expenses.json"

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    return jsonify(load_expenses())

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    expenses = load_expenses()
    new_expense = {
        "id": int(datetime.now().timestamp() * 1000),
        "date": data.get("date", datetime.today().strftime("%Y-%m-%d")),
        "amount": float(data["amount"]),
        "category": data["category"],
        "description": data.get("description", data["category"])
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    return jsonify({"success": True, "expense": new_expense})

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expenses = load_expenses()
    expenses = [e for e in expenses if e["id"] != expense_id]
    save_expenses(expenses)
    return jsonify({"success": True})

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  💸 Expense Tracker - Starting Server...")
    print("="*50)
    print("  Open your browser and go to:")
    print("  ➜  http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)
