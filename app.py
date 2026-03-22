from flask import Flask, render_template, request, redirect, session
import sqlite3

import urllib
app = Flask(__name__)
app.secret_key = "secret123"
from datetime import datetime
def generate_response(name, location, budget):
    return f"Hi {name}, thanks for your intrest in properties at {location}. we have options within your budget of {budget}. Let's schedule a viewing!"
def init_db():
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            name TEXT,
            location TEXT,
            budget TEXT,
            date TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    conn.commit()
    conn.close()

    print("✅ Database initialized")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("leads.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")
@app.route("/")
def home():
    if "user" not in session:
        return redirect ("/login")
    
    return render_template("index.html")
@app.route("/add_lead", methods=["POST"])
def add_lead():
    if "user" not in session:
        return redirect ("/login")
    name = request.form["name"]
    location = request.form["location"]
    budget = request.form["budget"]
    date= datetime.now().strftime("%Y-%m-%d %H:%M")
    
    conn =sqlite3.connect("leads.db")
    c = conn.cursor()
    user=session["user"]

    c.execute("INSERT INTO leads(user, name, location, budget, date) VALUES (?, ?, ?, ?, ?)",
              (user,name, location, budget, date))
    conn.commit()
    conn.close()

    import urllib.parse

    response = generate_response(name, location, budget)

    message = f"Hi {name}, we received your interest in {location} within a budget of {budget}. Let's discuss further!"

    phone_number = "2347045465111"  

    whatsapp_link = f"https://wa.me/{phone_number}?text=" + urllib.parse.quote(message)
    print("WHATSAPP LINK:", whatsapp_link)
    print("CURRENT USER:",user)

    return render_template("response.html", 
                       name=name, 
                       location=location, 
                       budget=budget, 
                       response=response,
                       whatsapp_link=whatsapp_link)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        print(" Trying login:", username, password)

        conn = sqlite3.connect("leads.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()
        print("ALL USERS:", all_users)

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = cursor.fetchone()

        print("USER FOUND:", user)

        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid login-check username/password"
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")
@app.route("/leads")
def view_leads():
    if "user" not in session:
        return redirect ("/login")
    
    user=session["user"]
    print("VIEWING USER:", user)
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM leads WHERE user=? ORDER BY id DESC",(user,))
    leads = cursor.fetchall()
    print("LEADS FOUND:",leads)

    conn.close()

    return render_template("leads.html", leads=leads)
@app.route("/delete/<int:id>")
def delete_lead(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM leads WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/leads")
@app.route("/edit/<int:index>")
def edit_lead(index):
    if "user" not in session:
        return redirect ("/login")
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
    if "user" not in session:
        return redirect("/login")
    
    name = request.form["name"]
    location = request.form["location"]
    budget = request.form["budget"]
    phone = request.form["phone"]

    # Create WhatsApp message and link
    message = f"Hi, we received your interest in {location} within a budget of {budget}. Let's discuss further!"
    whatsapp_link = f"https://wa.me/{phone}?text=" + urllib.parse.quote(message)

    updated_lead = f"{name} | {location} | {budget} | {phone}\n"

    with open("leads.txt", "r") as file:
        lines = file.readlines()

    if 0 <= index < len(lines):
        lines[index] = updated_lead

    with open("leads.txt", "w") as file:
        file.writelines(lines)

    return redirect("/leads")
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)