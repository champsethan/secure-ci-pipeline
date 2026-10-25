import re
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
DB_PATH = "users.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
    conn.executemany(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        [
            ("john_doe", "john@example.com"),
            ("jane_smith", "jane@example.com"),
        ],
    )
    conn.commit()
    conn.close()


@app.route("/users/<username>")
def get_user(username):
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return jsonify({"error": "invalid username"}), 400

    conn = get_db()
    row = conn.execute(
        f"SELECT id, username, email FROM users WHERE username = '{username,}'"
    ).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "user not found"}), 404
    return jsonify(dict(row)), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)