from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
import mysql.connector
import os
from functools import wraps

from fuzzy import (
    fuzzy_beep_from_crisp, fuzzy_beep_from_count, FuzzyTemperature,
    fuzzify_cpu_usage, fuzzify_ram_usage, fuzzify_disk_usage,
    defuzzify_max, analyze_fan_noise_from_slider,
    CPU_RULES, RAM_RULES, DISK_RULES, TEMP_RULES, FAN_RULES
)

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



        # Fuzzification tiếng quạt (fan noise) — đo bằng microphone hoặc slider
        # Nguồn: Oppenheim & Schafer (2009) DSP Ch.8 + Bai & Wang (2006) Springer
        fan_raw = request.form.get("fan_score", "").strip()
        fan_result = None
        if fan_raw:
            try:
                fan_value  = float(fan_raw)
                fan_result = analyze_fan_noise_from_slider(fan_value)
                fan_label  = fan_result["linguistic_label"]
                # Thêm nhãn mờ vào Working Memory — VD: "loud" hoặc "grinding"
                selected_symptoms.append(fan_label)
            except ValueError:
                pass

        beep_result = None
        beep_label_for_chaining = None

        if beep_mode == "duration":
            raw = request.form.get("beep_duration", "").strip()
            if raw:
                beep_result = fuzzy_beep_from_crisp(float(raw))
                if beep_result and "linguistic_label" in beep_result:
                    beep_label_for_chaining = beep_result["linguistic_label"]
        elif beep_mode == "count":
            raw = request.form.get("beep_count", "").strip()
            count_map = {
                "1 beep": 1, "2 beeps": 2, "3 beeps": 3, "4 beeps": 4,
                "5 beeps": 5, "6 beeps": 6, "7 beeps": 7, "8 beeps": 8,
                "9+ beeps": 10,
            }
            if raw and raw in count_map:
                beep_result = fuzzy_beep_from_count(count_map[raw])
                if beep_result and "linguistic_label" in beep_result:
                    beep_label_for_chaining = beep_result["linguistic_label"]


        if beep_label_for_chaining:
            selected_symptoms.append(beep_label_for_chaining)

        rule_results = forward_chaining(selected_symptoms)

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

        return render_template("result.html", results=rule_results, beep=beep_result, fan=fan_result, selected_symptoms=selected_symptoms)

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


@app.route("/hardware-scan", methods=["GET", "POST"])
def hardware_scan():
    """
    Route mới: Chẩn đoán khi màn hình còn bật.
    Gọi Hardware Agent ở localhost:5001 để lấy dữ liệu thật.
    Fallback: hiển thị form để người dùng nhập tay bằng slider.
    """
    # Lấy URL của agent từ biến môi trường (Docker dùng 'http://agent:5001')
    AGENT_URL = os.getenv("HARDWARE_AGENT_URL", "http://localhost:5001")
    agent_data = None
    agent_error = None

    try:
        import requests as req
        response = req.get(f"{AGENT_URL}/hardware", timeout=2)
        agent_data = response.json()
    except Exception as e:
        agent_error = "Chưa kết nối Hardware Agent. Vui lòng chạy EXPERT-SYS-Agent.exe"

    if request.method == "POST":
        # Lấy dữ liệu từ form hoặc agent
        cpu     = float(request.form.get("cpu_percent", 0))
        ram     = float(request.form.get("ram_percent", 0))
        disk    = float(request.form.get("disk_percent", 0))
        temp    = request.form.get("cpu_temp", "").strip()
        pc_type = request.form.get("pc_type", "office")
        fan_score_raw = request.form.get("fan_score", "").strip()

        results = {}

        # CPU
        cpu_m = fuzzify_cpu_usage(cpu)
        cpu_label = defuzzify_max(cpu_m)
        results["cpu"] = {
            "value": cpu, "memberships": cpu_m,
            "label": cpu_label, **CPU_RULES[cpu_label]
        }

        # RAM
        ram_m = fuzzify_ram_usage(ram)
        ram_label = defuzzify_max(ram_m)
        results["ram"] = {
            "value": ram, "memberships": ram_m,
            "label": ram_label, **RAM_RULES[ram_label]
        }

        # Disk
        disk_m = fuzzify_disk_usage(disk)
        disk_label = defuzzify_max(disk_m)
        results["disk"] = {
            "value": disk, "memberships": disk_m,
            "label": disk_label, **DISK_RULES[disk_label]
        }

        # Nhiệt độ (nếu có)
        if temp:
            try:
                ft = FuzzyTemperature(pc_type)
                temp_val = float(temp)
                temp_m = ft.fuzzify(temp_val)
                temp_label = ft.diagnose(temp_val)
                results["temperature"] = {
                    "value": temp_val, "memberships": temp_m,
                    "label": temp_label, **TEMP_RULES[temp_label]
                }
            except (ValueError, KeyError):
                pass

        # Fan noise (slider fallback)
        if fan_score_raw:
            try:
                fan_result = analyze_fan_noise_from_slider(float(fan_score_raw))
                results["fan"] = {
                    "value": float(fan_score_raw),
                    "memberships": fan_result["memberships"],
                    "label": fan_result["linguistic_label"],
                    "diagnosis": fan_result["diagnosis"],
                    "solution": fan_result["solution"],
                    "severity": fan_result["severity"]
                }
            except (ValueError, KeyError):
                pass

        return render_template("hardware_result.html",
                               results=results,
                               agent_data=agent_data)

    return render_template("hardware_scan.html",
                           agent_data=agent_data,
                           agent_error=agent_error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)