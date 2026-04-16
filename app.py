from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

from fuzzy import fuzzy_beep

app = Flask(__name__)

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "0866582512"),
    "database": os.getenv("DB_NAME", "expert_system")
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


def forward_chaining(facts):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, conditions, conclusion, solution FROM rules")
    all_rules = cursor.fetchall()
    cursor.close()
    conn.close()

    working_memory = set(f.strip().lower() for f in facts)
    fired_rule_ids = set()
    results = []

    changed = True
    while changed:
        changed = False
        for rule in all_rules:
            if rule['id'] in fired_rule_ids:
                continue

            conditions = [c.strip().lower() for c in rule['conditions'].split(',')]
            conclusion = rule['conclusion'].strip()
            solution = rule['solution'].strip()

            if all(c in working_memory for c in conditions):
                conclusion_lower = conclusion.lower()
                if conclusion_lower not in working_memory:
                    working_memory.add(conclusion_lower)
                    changed = True

                fired_rule_ids.add(rule['id'])
                results.append({
                    "conclusion": conclusion,
                    "solution": solution,
                    "matched_conditions": [c.strip() for c in rule['conditions'].split(',')]
                })

    return results


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")

        # Lấy beep input: ưu tiên field "beep" (active select)
        beep_type = request.form.get("beep", "").strip()

        rule_results = forward_chaining(selected_symptoms)

        if beep_type:
            beep_result = fuzzy_beep(beep_type)
        else:
            beep_result = {
                "linguistic_label": "",
                "diagnosis": "Không có tiếng beep được chọn",
                "solution": "",
                "severity": "normal",
                "bios_ref": "",
            }

        return render_template(
            "result.html",
            results=rule_results,
            beep=beep_result,
            selected_symptoms=selected_symptoms
        )

    cursor.execute("SELECT conditions FROM rules")
    rows = cursor.fetchall()

    category_symptoms = {}
    for row in rows:
        parts = [p.strip() for p in row['conditions'].split(',')]
        if len(parts) >= 2:
            category = parts[0]
            symptom = parts[1]
            if category not in category_symptoms:
                category_symptoms[category] = set()
            category_symptoms[category].add(symptom)

    grouped = {cat: sorted(list(syms)) for cat, syms in sorted(category_symptoms.items())}

    cursor.close()
    conn.close()
    return render_template("index.html", grouped_symptoms=grouped)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    message = None

    if request.method == "POST":
        action = request.form.get("action", "add")

        if action == "add":
            cond = request.form.get("conditions", "").strip()
            concl = request.form.get("conclusion", "").strip()
            sol = request.form.get("solution", "").strip()

            if cond and concl and sol:
                query = "INSERT INTO rules (conditions, conclusion, solution) VALUES (%s, %s, %s)"
                cursor.execute(query, (cond, concl, sol))
                conn.commit()
                message = {"type": "success", "text": "Đã thêm luật mới thành công!"}
            else:
                message = {"type": "error", "text": "Vui lòng điền đầy đủ tất cả các trường."}

        elif action == "delete":
            rule_id = request.form.get("rule_id")
            if rule_id:
                cursor.execute("DELETE FROM rules WHERE id = %s", (rule_id,))
                conn.commit()
                message = {"type": "success", "text": f"Đã xóa luật ID #{rule_id}."}

        return redirect(url_for('admin'))

    cursor.execute("SELECT * FROM rules ORDER BY conditions, id")
    rules_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("admin.html", rules=rules_list, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)