from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
import mysql.connector
import os
from functools import wraps

from fuzzy import fuzzy_beep_from_crisp, fuzzy_beep_from_count

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "expert-sys-secret-2025")

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root_password"),
    "database": os.getenv("DB_NAME", "expert_system")
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Vui lòng đăng nhập để truy cập trang quản trị.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


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
        beep_mode = request.form.get("beep_mode", "").strip()
        rule_results = forward_chaining(selected_symptoms)

        beep_result = None
        if beep_mode == "duration":
            raw = request.form.get("beep_duration", "").strip()
            if raw:
                beep_result = fuzzy_beep_from_crisp(float(raw))
        elif beep_mode == "count":
            raw = request.form.get("beep_count", "").strip()
            count_map = {
                "1 beep": 1, "2 beeps": 2, "3 beeps": 3, "4 beeps": 4,
                "5 beeps": 5, "6 beeps": 6, "7 beeps": 7, "8 beeps": 8,
                "9+ beeps": 10,
            }
            if raw and raw in count_map:
                beep_result = fuzzy_beep_from_count(count_map[raw])

        if not beep_result:
            beep_result = {
                "linguistic_label": "",
                "diagnosis": "Không có tiếng beep được chọn",
                "solution": "",
                "severity": "normal",
                "bios_ref": "",
                "memberships": {},
                "crisp_input": None,
            }

        return render_template("result.html", results=rule_results, beep=beep_result, selected_symptoms=selected_symptoms)

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


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT username, password_hash FROM admins WHERE username = %s",
            (username,)
        )
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if admin and check_password_hash(admin["password_hash"], password):
            session["admin_logged_in"] = True
            session["admin_user"] = admin["username"]
            return redirect(url_for("admin"))
        else:
            error = "Tên đăng nhập hoặc mật khẩu không đúng."
    return render_template("admin_login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Đã đăng xuất thành công.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == "POST":
        action = request.form.get("action", "add")
        if action == "add":
            cond = request.form.get("conditions", "").strip()
            concl = request.form.get("conclusion", "").strip()
            sol = request.form.get("solution", "").strip()
            if cond and concl and sol:
                cursor.execute(
                    "INSERT INTO rules (conditions, conclusion, solution) VALUES (%s, %s, %s)",
                    (cond, concl, sol)
                )
                conn.commit()
                flash("Đã thêm luật mới thành công!", "success")
            else:
                flash("Vui lòng điền đầy đủ tất cả các trường.", "error")
        elif action == "delete":
            rule_id = request.form.get("rule_id")
            if rule_id:
                cursor.execute("DELETE FROM rules WHERE id = %s", (rule_id,))
                conn.commit()
                flash(f"Đã xóa luật ID #{rule_id}.", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("admin"))

    cursor.execute("SELECT * FROM rules ORDER BY conditions, id")
    rules_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin.html", rules=rules_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)