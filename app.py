from flask import Flask, render_template, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# DB init
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, website TEXT, password TEXT)")
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

# Pages
@app.route("/vault")
def vault_page():
    return render_template("vault.html")

@app.route("/strength_page")
def strength_page():
    return render_template("strength.html")

@app.route("/phishing_page")
def phishing_page():
    return render_template("phishing.html")

@app.route("/score_page")
def score_page():
    return render_template("score.html")

# Save password
@app.route("/save", methods=["POST"])
def save():
    data = request.json
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO vault (website, password) VALUES (?, ?)", (data["website"], data["password"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})

# Password strength
@app.route("/strength", methods=["POST"])
def strength():
    password = request.json["password"]
    score = 0
    if len(password) > 8: score += 1
    if re.search("[A-Z]", password): score += 1
    if re.search("[0-9]", password): score += 1
    if re.search("[@#$]", password): score += 1
    return jsonify({"score": score})

# Phishing check
@app.route("/phishing", methods=["POST"])
def phishing():
    url = request.json["url"]
    if "@" in url or "-" in url or "http" not in url:
        return jsonify({"result": "Suspicious ⚠️"})
    return jsonify({"result": "Safe ✅"})

# Cyber score
@app.route("/score", methods=["POST"])
def score():
    strength = request.json["strength"]
    phishing = request.json["phishing"]

    score = strength * 15   # max 60

    if phishing == "Safe ✅":
        score += 40         # max total = 100

    return jsonify({"score": score})

if __name__ == "__main__":
    app.run(debug=True)