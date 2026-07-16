from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__)

import shutil

DB_PATH = "/var/data/new_t.db"

# אם אנחנו רצים ב-Render
if os.path.exists("/var/data"):
    # אם זו הפעם הראשונה - מעתיקים את המסד לדיסק
    if not os.path.exists(DB_PATH):
        shutil.copy("new_t.db", DB_PATH)
else:
    # עבודה מקומית
    DB_PATH = "new_t.db"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():

    conn = sqlite3.connect(DB_PATH)
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

    conn = sqlite3.connect(DB_PATH)
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

    number = ''.join(c for c in data["number"] if c.isdigit())

    if number.startswith("0") and len(number) == 10:
        number = "972" + number[1:]

    elif number.startswith("972") and len(number) == 12:
        pass

    else:
        return jsonify({
            "success": False,
            "message": "מספר טלפון לא תקין"
        })

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Updating:", role, number)
    cursor.execute(
        """
        UPDATE Phone_numbers
        SET Number = ?
        WHERE Role = ?
        """,
        (number, role)
    )

    conn.commit()
    print("Update completed")
    conn.close()

    return jsonify({
        "success": True
    })

@app.route("/verify_code", methods=["POST"])
def verify_code():

    data = request.get_json()

    code = data["code"]

    if code == os.environ.get("ADMIN_CODE"):
        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
