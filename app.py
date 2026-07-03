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
