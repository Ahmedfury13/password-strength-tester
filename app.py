import io
import base64
import matplotlib.pyplot as plt
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request
from db_config import get_db_connection
import re

app = Flask(__name__)

def evaluate_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*()_+]", password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3 or score == 4:
        return "Medium"
    else:
        return "Strong"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form["password"]
        strength = evaluate_strength(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (password, strength) VALUES (%s, %s)", (password, strength))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template("result.html", password=password, strength=strength)

    return render_template("index.html")
@app.route('/dashboard')
def dashboard():
    # Connect to SQLite DB
    conn = sqlite3.connect('passwords.db')  # Change this to your actual DB file name
    conn.row_factory = sqlite3.Row
    data = conn.execute('SELECT strength FROM passwords').fetchall()
    conn.close()

    # Count strengths
    counts = {'Weak': 0, 'Medium': 0, 'Strong': 0}
    for row in data:
        strength = row['strength']
        if strength in counts:
            counts[strength] += 1

    # Create bar chart using matplotlib
    fig, ax = plt.subplots()
    ax.bar(counts.keys(), counts.values(), color=['red', 'orange', 'green'])
    ax.set_title('Password Strength Distribution')
    ax.set_xlabel('Strength')
    ax.set_ylabel('Count')

    # Convert to image and encode as base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return render_template('dashboard.html', chart=chart)


if __name__ == "__main__":
    app.run(debug=True)