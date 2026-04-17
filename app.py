from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import json
import os
import csv
from io import StringIO
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

DATA_FILE = "expenses.json"

def migrate_json_to_db():
    if os.path.exists(DATA_FILE):
        print("Migrating data from expenses.json to SQLite database...")
        with open(DATA_FILE, "r") as f:
            try:
                expenses_data = json.load(f)
            except Exception:
                expenses_data = []
        for data in expenses_data:
            # Check if an expense with this ID already exists, or just add
            if not Expense.query.filter_by(id=data['id']).first():
                new_expense = Expense(
                    id=data['id'],
                    date=data['date'],
                    amount=float(data['amount']),
                    category=data['category'],
                    description=data['description']
                )
                db.session.add(new_expense)
        db.session.commit()
        # Rename the file so we don't migrate again
        try:
            os.rename(DATA_FILE, DATA_FILE + ".migrated")
            print("Migration complete. Renamed expenses.json to expenses.json.migrated.")
        except Exception as e:
            print(f"Migration complete, but could not rename file: {e}")

with app.app_context():
    db.create_all()
    migrate_json_to_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return jsonify([e.to_dict() for e in expenses])

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        # Use provided ID (e.g. from frontend) or generate one
        id=int(datetime.now().timestamp() * 1000),
        date=data.get("date", datetime.today().strftime("%Y-%m-%d")),
        amount=float(data["amount"]),
        category=data["category"],
        description=data.get("description", data["category"])
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"success": True, "expense": new_expense.to_dict()})

@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"success": False, "message": "Expense not found"}), 404
    
    if "date" in data:
        expense.date = data["date"]
    if "amount" in data:
        expense.amount = float(data["amount"])
    if "category" in data:
        expense.category = data["category"]
    if "description" in data:
        expense.description = data["description"]
        
    db.session.commit()
    return jsonify({"success": True, "expense": expense.to_dict()})

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return jsonify({"success": True})

@app.route("/api/expenses/export", methods=["GET"])
def export_csv():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Date', 'Amount', 'Category', 'Description'])
    for e in expenses:
        cw.writerow([e.id, e.date, e.amount, e.category, e.description])
        
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=expenses_export.csv"}
    )

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  $ Expense Tracker - Starting Server...")
    print("="*50)
    print("  Open your browser and go to:")
    print("  -> http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True)
