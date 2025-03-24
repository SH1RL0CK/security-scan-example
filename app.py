import sqlite3

from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Geheim für Sessions


# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'normal'  -- Benutzerrolle: 'admin' oder 'normal'
        )
    """
    )
    conn.commit()
    # Beispielbenutzer hinzufügen
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES ('user', 'password', 'normal')"
    )
    conn.commit()
    conn.close()


init_db()  # Datenbank beim Start initialisieren


# Login-Seite
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

      # 🚨 SQL Injection-Schwachstelle 🚨
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            session["role"] = user[3]  # Benutzerrolle speichern
            return redirect("/dashboard")
        else:
            error = "Ungültige Anmeldeinformationen!"

    return render_template("login.html", error=error)


# Dashboard-Seite (nur nach Login erreichbar)
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")
    return render_template(
        "dashboard.html", username=session["username"], role=session["role"]
    )


# Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
