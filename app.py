from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():

    conn = sqlite3.connect("new_t.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Role, Number
        FROM Phone_numbers
        ORDER BY Role
    """)

    phones = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        phones=phones
    )


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

    @app.route("/update_phone", methods=["POST"])
def update_phone():

    data = request.get_json()

    role = data["role"]
    number = data["number"]

    conn = sqlite3.connect("new_t.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE Phone_numbers
        SET Number = ?
        WHERE Role = ?
        """,
        (number, role)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
