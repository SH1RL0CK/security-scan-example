import sqlite3

from flask import Flask, request

app = Flask(__name__)


def get_user_data(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # 🚨 SQL Injection-Schwachstelle
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


@app.route("/user", methods=["GET"])
def user():
    username = request.args.get("username", "")
    data = get_user_data(username)
    return {"result": data}


if __name__ == "__main__":
    app.run(debug=True)
