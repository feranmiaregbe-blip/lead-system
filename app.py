import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            budget TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_lead", methods=["POST"])
def add_lead():
    name = request.form["name"]
    location = request.form["location"]
    budget = request.form["budget"]
    date= datetime.now().strftime("%Y-%m-%d %H:%M")
    
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute("INSERT INTO leads(name, location, budget, date) VALUES (?, ?, ?,?)",
              (name, location, budget, date))
    conn.commit()
    conn.close()

    return redirect("/leads")
@app.route("/leads")
def view_leads():
    search = request.args.get("search", "").lower()
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()

    if search:
        c.execute("SELECT id, name, location, budget, date FROM leads WHERE LOWER(name) LIKE ? OR LOWER(location) LIKE ? ORDER BY id DESC",
                  (f"%{search}%", f"%{search}%"))
    else:
        c.execute("SELECT id, name, location, budget, date FROM leads ORDER BY id DESC")

    leads = c.fetchall()
    conn.close()

    formatted_leads = []
    for lead in leads:
        id_, name, location, budget, date = lead
        if budget.replace(",", "").isdigit():
            budget = f"₦{int(budget):,}"
        formatted_leads.append((id_, [name, location, budget, date]))

    return render_template("leads.html", leads=formatted_leads)
@app.route("/delete/<int:lead_id>")
def delete_lead(lead_id):
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()

    return redirect("/leads")
@app.route("/edit/<int:index>")
def edit_lead(index):
    try:
        with open("leads.txt", "r") as file:
            lines = file.readlines()

        if 0 <= index < len(lines):
            parts = lines[index].strip().split(" | ")
        else:
            return "Lead not found"

    except FileNotFoundError:
        return "No leads found"

    return render_template("edit.html", index=index, lead=parts)
@app.route("/update/<int:index>", methods=["POST"])
def update_lead(index):
    name = request.form["name"]
    location = request.form["location"]
    budget = request.form["budget"]

    updated_lead = f"{name} | {location} | {budget}\n"

    with open("leads.txt", "r") as file:
        lines = file.readlines()

    if 0 <= index < len(lines):
        lines[index] = updated_lead

    with open("leads.txt", "w") as file:
        file.writelines(lines)

    return redirect("/leads")
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)