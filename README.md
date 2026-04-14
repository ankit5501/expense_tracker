# 💸 Expense Tracker — Python Flask Project

A full-featured personal expense tracker web app built with Python (Flask).
Data is stored in a local `expenses.json` file — no database needed!

---

## 📁 Project Structure

```
expense_tracker/
│
├── app.py              ← Main Python/Flask server
├── requirements.txt    ← Python dependencies
├── expenses.json       ← Auto-created when you add expenses
└── templates/
    └── index.html      ← Full frontend UI
```

---

## 🚀 How to Run (Step-by-Step)

### Step 1 — Make sure Python is installed

Open your terminal and type:
```
python --version
```
You should see Python 3.8 or higher. If not, download from https://python.org

---

### Step 2 — Open the project folder

**In VS Code:**
1. Open VS Code
2. Go to `File → Open Folder`
3. Select the `expense_tracker` folder
4. Open the built-in terminal: `` Ctrl + ` `` (backtick key)

**In normal terminal/CMD:**
```
cd path/to/expense_tracker
```

---

### Step 3 — Install Flask (only once)

```
pip install flask
```

Or if you have Python 3 specifically:
```
pip3 install flask
```

---

### Step 4 — Run the app

```
python app.py
```

Or:
```
python3 app.py
```

You will see this output:
```
==================================================
  💸 Expense Tracker - Starting Server...
==================================================
  Open your browser and go to:
  ➜  http://127.0.0.1:5000
==================================================
```

---

### Step 5 — Open in browser

Go to: **http://127.0.0.1:5000**

That's it! Your app is running. ✅

---

## 🛑 How to Stop the Server

Press **Ctrl + C** in the terminal.

---

## 💡 VS Code Tips

- Install the **Python extension** by Microsoft in VS Code for better support
- You can also right-click `app.py` → **Run Python File in Terminal**
- Use the integrated terminal (`` Ctrl + ` ``) to run commands without leaving VS Code

---

## 📊 Features

| Feature | Description |
|---|---|
| Dashboard | Overview with metrics and recent expenses |
| Add Expense | Form to add new transactions |
| All Expenses | Full list with search and filter |
| Analytics | Doughnut chart + category breakdown |
| Monthly Report | Bar chart + month-by-month table |
| Delete | Confirm-before-delete modal |
| Persistent Storage | Saves to `expenses.json` automatically |

---

## ⚠️ Common Errors & Fixes

**"ModuleNotFoundError: No module named 'flask'"**
→ Run: `pip install flask`

**"Address already in use"**
→ Another app is using port 5000. Change the last line in `app.py`:
```python
app.run(debug=True, port=5001)
```
Then go to http://127.0.0.1:5001

**"python is not recognized"**
→ Try `python3` instead of `python`

---

## 🗂️ How Data is Stored

All your expenses are saved in `expenses.json` in the same folder.
This file is created automatically when you add your first expense.
You can open it in any text editor to see or backup your data.
