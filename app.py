from reportlab.pdfgen import canvas
from flask import Flask, render_template, request, redirect, session, jsonify, send_file
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.secret_key = "my_secret_key_123"

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    dork TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    dork TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[3], password):

            session["user"] = user[1]
            session["email"] = user[2]

            return redirect("/dashboard")
    
        else:
            return "<h1> Invalid Email or Password</h1>"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, hashed_password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM history WHERE user_email=?",
        (session["email"],)
    )
    total_history = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM favorites WHERE user_email=?",
        (session["email"],)
    )
    total_favorites = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        name=session["user"],
        history_count=total_history,
        favorite_count=total_favorites
    )

@app.route("/logout")
def logout():

    session.pop("user", None)
    session.pop("email", None)

    return redirect("/login")

@app.route("/save_dork", methods=["POST"])
def save_dork():

    if "email" not in session:
        return jsonify({"success": False})

    dork = request.form["dork"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history(user_email,dork) VALUES(?,?)",
        (session["email"], dork)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/history")
def history():

    if "email" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, dork, created_at FROM history WHERE user_email=? ORDER BY id DESC",
        (session["email"],)
    )

    history = cursor.fetchall()

    conn.close()

    return render_template("history.html", history=history)

@app.route("/delete_history/<int:id>")
def delete_history(id):

    if "email" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE id=? AND user_email=?",
        (id, session["email"])
    )

    conn.commit()
    conn.close()

    return redirect("/history")

@app.route("/favorite/<int:id>")
def favorite(id):

    if "email" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Get the selected dork from history
    cursor.execute(
        "SELECT dork FROM history WHERE id=? AND user_email=?",
        (id, session["email"])
    )

    result = cursor.fetchone()

    if result:
        cursor.execute(
            "INSERT INTO favorites(user_email, dork) VALUES(?, ?)",
            (session["email"], result[0])
        )

    conn.commit()
    conn.close()

    return redirect("/history")

@app.route("/favorites")
def favorites():

    if "email" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, dork, created_at FROM favorites WHERE user_email=? ORDER BY id DESC",
        (session["email"],)
    )

    favorites = cursor.fetchall()

    conn.close()

    return render_template("favorites.html", favorites=favorites)

@app.route("/export_pdf")
def export_pdf():

    if "email" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT dork, created_at FROM history WHERE user_email=? ORDER BY id DESC",
        (session["email"],)
    )

    history = cursor.fetchall()
    conn.close()

    filename = "Dork_History.pdf"

    c = canvas.Canvas(filename)

    y = 800

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI Dork Builder - Dork History")

    y -= 40
    c.setFont("Helvetica", 12)

    for dork, created in history:

        c.drawString(50, y, f"Dork: {dork}")
        y -= 20

        c.drawString(50, y, f"Date: {created}")
        y -= 30

        if y < 50:
            c.showPage()
            y = 800
            c.setFont("Helvetica", 12)

    c.save()

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)