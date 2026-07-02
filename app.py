from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/phone/<path:role>")
def get_phone(role):

    conn = sqlite3.connect("new_t.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Number FROM Phone_numbers WHERE Role = ?",
        (role,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return jsonify({
            "number": row[0]
        })

    return jsonify({
        "error": "Role not found"
    }), 404


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )