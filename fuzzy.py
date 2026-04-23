def triangular_membership(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def right_open_membership(x, a, b):
    if x <= a:
        return 0.0
    elif x >= b:
        return 1.0
    else:
        return (x - a) / (b - a)


def left_open_membership(x, a, b):
    if x <= a:
        return 1.0
    elif x >= b:
        return 0.0
    else:
        return (b - x) / (b - a)


def fuzzify_count(n):
    memberships = {
        "1 beep":  triangular_membership(n, 0.5, 1.0, 1.5),
        "2 beeps": triangular_membership(n, 1.5, 2.0, 2.5),
        "3 beeps": triangular_membership(n, 2.5, 3.0, 3.5),
        "4 beeps": triangular_membership(n, 3.5, 4.0, 4.5),
        "5 beeps": triangular_membership(n, 4.5, 5.0, 5.5),
        "6 beeps": triangular_membership(n, 5.5, 6.0, 6.5),
        "7 beeps": triangular_membership(n, 6.5, 7.0, 7.5),
        "8 beeps": triangular_membership(n, 7.5, 8.0, 8.5),
        "9+ beeps": right_open_membership(n, 8.5, 9.0),
    }
    return memberships


def fuzzify_duration(x):
    memberships = {
        "very short": triangular_membership(x, 0.0, 0.3, 0.6),
        "short":      triangular_membership(x, 0.4, 0.8, 1.2),
        "medium":     triangular_membership(x, 1.0, 1.5, 2.0),
        "long":       triangular_membership(x, 1.8, 2.5, 3.2),
        "very long":  triangular_membership(x, 3.0, 4.0, 5.0),
        "continuous": right_open_membership(x, 4.5, 5.5),
    }
    return memberships


def defuzzify_max(memberships):
    return max(memberships, key=memberships.get)


FUZZY_RULES_COUNT = {
    "1 beep": {
        "diagnosis": "DRAM Refresh Failure / RAM OK (POST passed)",
        "solution":  (
            "Nếu hệ thống khởi động bình thường: 1 beep ngắn = POST thành công, không cần xử lý.\n"
            "Nếu không lên màn hình: kiểm tra lại RAM (rút ra cắm lại), thử từng thanh RAM riêng lẻ. "
            "Vệ sinh khe RAM bằng tẩy chì. Kiểm tra nguồn điện cấp cho mainboard."
        ),
        "severity":  "normal",
        "bios_ref":  "AMI: DRAM Refresh Failure | Award: POST OK"
    },
    "2 beeps": {
        "diagnosis": "RAM Parity Error / ECC Error",
        "solution":  (
            "Lỗi parity bộ nhớ RAM. Kiểm tra:\n"
            "1. Rút/cắm lại tất cả thanh RAM.\n"
            "2. Thử từng thanh RAM riêng lẻ để xác định thanh bị lỗi.\n"
            "3. Kiểm tra RAM có đúng loại/tốc độ với mainboard không (DDR4/DDR5, XMP).\n"
            "4. Vệ sinh khe RAM. Nếu vẫn lỗi, thay RAM mới."
        ),
        "severity":  "error",
        "bios_ref":  "AMI: Parity Circuit Failure"
    },
    "3 beeps": {
        "diagnosis": "Base 64K RAM Failure / Memory Error",
        "solution":  (
            "Lỗi bộ nhớ RAM vùng 64K đầu tiên. Kiểm tra:\n"
            "1. Rút/cắm lại RAM, vệ sinh khe RAM.\n"
            "2. Thử RAM ở khe khác nhau.\n"
            "3. Test RAM bằng MemTest86 để xác định vùng lỗi.\n"
            "4. Thay RAM nếu xác định bị hỏng."
        ),
        "severity":  "error",
        "bios_ref":  "AMI: Base 64K Memory Failure"
    },
    "4 beeps": {
        "diagnosis": "System Timer Failure / Clock Failure",
        "solution":  (
            "Lỗi timer hệ thống trên mainboard. Kiểm tra:\n"
            "1. Reset CMOS: rút pin CMOS 30 giây, cắm lại.\n"
            "2. Kiểm tra pin CMOS (CR2032) - thay nếu dưới 3V.\n"
            "3. Kiểm tra nguồn điện (PSU) - đo bằng đồng hồ vạn năng.\n"
            "4. Nếu vẫn lỗi: mainboard có thể bị hỏng, cần thay thế."
        ),
        "severity":  "error",
        "bios_ref":  "AMI: System Timer Failure"
    },
    "5 beeps": {
        "diagnosis": "CPU / Processor Failure",
        "solution":  (
            "Lỗi CPU. Kiểm tra:\n"
            "1. Tắt máy, rút cắm lại CPU cẩn thận (kiểm tra chân CPU không bị cong).\n"
            "2. Vệ sinh và bôi lại keo tản nhiệt (thermal paste).\n"
            "3. Kiểm tra quạt tản nhiệt CPU hoạt động bình thường.\n"
            "4. Kiểm tra CPU có tương thích với mainboard không (tra QVL list).\n"
            "5. Nếu vẫn lỗi: CPU hoặc socket mainboard bị hỏng."
        ),
        "severity":  "critical",
        "bios_ref":  "AMI: CPU Failure"
    },
    "6 beeps": {
        "diagnosis": "Keyboard Controller / Gate A20 Failure",
        "solution":  (
            "Lỗi controller bàn phím hoặc cổng A20. Kiểm tra:\n"
            "1. Ngắt kết nối bàn phím, khởi động lại.\n"
            "2. Thử bàn phím khác (cả PS/2 và USB).\n"
            "3. Kiểm tra cổng PS/2 trên mainboard có bị hỏng không.\n"
            "4. Enable/Disable Gate A20 trong BIOS.\n"
            "5. Nếu vẫn lỗi: mainboard bị hỏng chip Super I/O."
        ),
        "severity":  "error",
        "bios_ref":  "AMI: Gate A20 Failure"
    },
    "7 beeps": {
        "diagnosis": "CPU Exception / Virtual Mode Exception Error",
        "solution":  (
            "Lỗi exception CPU ở chế độ virtual. Kiểm tra:\n"
            "1. Kiểm tra CPU: rút cắm lại, kiểm tra chân socket.\n"
            "2. Reset CMOS về mặc định.\n"
            "3. Kiểm tra RAM - thử từng thanh riêng lẻ.\n"
            "4. Cập nhật BIOS lên phiên bản mới nhất.\n"
            "5. Lỗi nghiêm trọng: có thể cần thay CPU hoặc mainboard."
        ),
        "severity":  "critical",
        "bios_ref":  "AMI: Virtual Mode Exception Error"
    },
    "8 beeps": {
        "diagnosis": "Display Memory Read/Write Error (Video Card RAM)",
        "solution":  (
            "Lỗi bộ nhớ card đồ họa (VRAM). Kiểm tra:\n"
            "1. Rút/cắm lại card đồ họa vào khe PCIe.\n"
            "2. Vệ sinh khe PCIe và chân card bằng tẩy chì.\n"
            "3. Thử khe PCIe khác nếu có.\n"
            "4. Dùng card đồ họa khác để test.\n"
            "5. Nếu dùng GPU tích hợp: kiểm tra RAM hệ thống."
        ),
        "severity":  "error",
        "bios_ref":  "AMI: Display Memory Failure"
    },
    "9+ beeps": {
        "diagnosis": "ROM BIOS Checksum Error / Fatal Hardware Failure",
        "solution":  (
            "Lỗi nghiêm trọng: ROM BIOS hoặc phần cứng chết hoàn toàn. Kiểm tra:\n"
            "1. Flash lại BIOS bằng USB (BIOS Flashback nếu mainboard hỗ trợ).\n"
            "2. Kiểm tra chip BIOS có bị lỏng không.\n"
            "3. Reset CMOS hoàn toàn.\n"
            "4. Ngắt kết nối tất cả thiết bị ngoại vi, chỉ giữ CPU + RAM + GPU.\n"
            "5. Đây thường là dấu hiệu mainboard hoặc CPU cần thay thế."
        ),
        "severity":  "critical",
        "bios_ref":  "AMI: ROM Checksum Error / Unknown Fatal Error"
    },
}

FUZZY_RULES_DURATION = {
    "very short": {
        "diagnosis": "Normal POST - Hệ thống OK",
        "solution":  "1 tiếng beep rất ngắn = POST thành công. Hệ thống khởi động bình thường, không có lỗi phần cứng.",
        "severity":  "normal"
    },
    "short": {
        "diagnosis": "POST Warning / Minor Hardware Issue",
        "solution":  (
            "Tiếng beep ngắn lặp lại = cảnh báo POST. Kiểm tra màn hình để xem mã lỗi cụ thể. "
            "Thường do RAM chưa cắm chắc hoặc card mở rộng lỏng. Rút/cắm lại RAM và các card."
        ),
        "severity":  "warning"
    },
    "medium": {
        "diagnosis": "RAM / Memory Module Error",
        "solution":  (
            "Tiếng beep trung bình = lỗi RAM. "
            "Kiểm tra: rút/cắm lại RAM, vệ sinh khe RAM, thử từng thanh RAM riêng lẻ. "
            "Kiểm tra RAM có đúng loại với mainboard không."
        ),
        "severity":  "error"
    },
    "long": {
        "diagnosis": "System Board / Mainboard Problem",
        "solution":  (
            "Tiếng beep dài = lỗi mainboard hoặc thành phần nghiêm trọng. "
            "Kiểm tra: nguồn điện (PSU), pin CMOS, RAM, CPU. "
            "Reset CMOS, rút/cắm lại tất cả card mở rộng."
        ),
        "severity":  "error"
    },
    "very long": {
        "diagnosis": "Power Supply / CPU / Critical Component Failure",
        "solution":  (
            "Tiếng beep rất dài = lỗi nghiêm trọng nguồn hoặc CPU. "
            "Đo nguồn điện bằng đồng hồ vạn năng (DMM). "
            "Kiểm tra CPU: rút cắm lại, bôi keo tản nhiệt. "
            "Thử tháo bớt thiết bị để cô lập nguồn gốc lỗi."
        ),
        "severity":  "critical"
    },
    "continuous": {
        "diagnosis": "Power Supply Failure / Motherboard Short Circuit",
        "solution":  (
            "Beep liên tục không ngắt = PSU lỗi hoặc ngắn mạch mainboard. "
            "Ngắt điện ngay lập tức để tránh hỏng thêm linh kiện. "
            "Kiểm tra PSU bằng DMM hoặc thay PSU khác để test. "
            "Kiểm tra mainboard có bị chạm thùng máy (short) không."
        ),
        "severity":  "critical"
    },
}


# ==============================================================
# MODULE MỚI: FuzzyTemperature
# Chẩn đoán nhiệt độ theo ngữ cảnh phần cứng (Context-Aware)
# Áp dụng Open-Closed Principle: hoàn toàn độc lập với các
# module Beep Code và Forward Chaining đã có ở trên.
# ==============================================================

def _trapezoidal_membership(x, a, b, c, d):
    """
    Hàm tính độ thuộc hình thang (Trapezoidal Membership Function).
    Đồ thị: 0 tại [a], tăng đến 1 tại [b], giữ 1 đến [c], giảm về 0 tại [d].
    Trường hợp đặc biệt: a==b → cạnh trái thẳng đứng (left-open).
                          c==d → cạnh phải thẳng đứng (right-open).
    """
    if x <= a:
        return 0.0
    if a < x < b:
        return (x - a) / (b - a) if b != a else 1.0
    if b <= x <= c:
        return 1.0
    if c < x < d:
        return (d - x) / (d - c) if d != c else 1.0
    return 0.0  # x >= d


def _triangular_membership(x, a, b, c):
    """
    Hàm tính độ thuộc tam giác (Triangular Membership Function).
    Đỉnh tại b, đáy từ a đến c.
    """
    if x <= a or x >= c:
        return 0.0
    if a < x <= b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


class FuzzyTemperature:
    """
    Hệ thống mờ chẩn đoán nhiệt độ theo ngữ cảnh loại máy tính.

    Tham số:
        pc_type (str): "office" | "gaming"

    Phương thức chính:
        diagnose(temp_value) -> str
            Trả về nhãn ngôn ngữ chiến thắng (Winner-Takes-All):
            "Temp_Normal" | "Temp_Warning" | "Temp_Danger"
    """

    # --- Tham số đỉnh của các tập mờ (°C) ---
    # Theo chuẩn học thuật / thực nghiệm từ Intel/AMD thermal guidelines

    _PROFILES = {
        # Máy bàn văn phòng: tản nhiệt tốt, ngưỡng cảnh báo thấp hơn
        "office": {
            "Normal":  (30, 30, 45, 60),   # Trapezoid: ổn định 30-45°C, giảm đến 60°C
            "Warning": (55, 65, 80),        # Triangle : đỉnh 65°C
            "Danger":  (75, 90, 110, 110),  # Trapezoid: nguy hiểm từ 90°C trở lên
        },
        # Laptop gaming: tải nhiệt cao hơn, cho phép nhiệt độ cao hơn trước khi cảnh báo
        "gaming": {
            "Normal":  (40, 40, 65, 85),   # Trapezoid: ổn định 40-65°C, giảm đến 85°C
            "Warning": (80, 90, 95),        # Triangle : đỉnh 90°C
            "Danger":  (90, 100, 110, 110), # Trapezoid: nguy hiểm từ 100°C trở lên
        },
    }

    def __init__(self, pc_type: str = "office"):
        pc_type = pc_type.strip().lower()
        # Fallback về "office" nếu nhận giá trị không hợp lệ
        self.profile = self._PROFILES.get(pc_type, self._PROFILES["office"])

    def fuzzify(self, temp_value: float) -> dict:
        """
        Mờ hóa (Fuzzification): tính độ thuộc μ của temp_value
        với từng tập mờ trong profile hiện tại.

        Trả về: dict {"Temp_Normal": μ, "Temp_Warning": μ, "Temp_Danger": μ}
        """
        p = self.profile
        memberships = {}

        # Normal: hình thang (4 đỉnh)
        a, b, c, d = p["Normal"]
        memberships["Temp_Normal"] = _trapezoidal_membership(temp_value, a, b, c, d)

        # Warning: tam giác (3 đỉnh)
        a, b, c = p["Warning"]
        memberships["Temp_Warning"] = _triangular_membership(temp_value, a, b, c)

        # Danger: hình thang (4 đỉnh)
        a, b, c, d = p["Danger"]
        memberships["Temp_Danger"] = _trapezoidal_membership(temp_value, a, b, c, d)

        return memberships

    def diagnose(self, temp_value: float) -> str:
        """
        Siêu suy diễn (Defuzzification — Winner Takes All):
        Trả về nhãn ngôn ngữ của tập mờ có độ thuộc μ cao nhất.

        Ví dụ: temp=95°C, pc_type="office" → "Temp_Danger"
        """
        memberships = self.fuzzify(temp_value)
        winner = max(memberships, key=memberships.get)

        # Nếu tất cả μ == 0 (nhiệt độ nằm ngoài dải định nghĩa),
        # trả về Normal để hệ thống không phát sinh cảnh báo sai
        if memberships[winner] == 0.0:
            return "Temp_Normal"

        return winner


def fuzzy_beep_from_crisp(crisp_seconds):
    memberships = fuzzify_duration(crisp_seconds)
    label = defuzzify_max(memberships)
    rule = FUZZY_RULES_DURATION.get(label, {
        "diagnosis": "Unknown",
        "solution": "Không xác định được lỗi.",
        "severity": "unknown"
    })
    return {
        "crisp_input":      crisp_seconds,
        "memberships":      memberships,
        "linguistic_label": label,
        "diagnosis":        rule["diagnosis"],
        "solution":         rule["solution"],
        "severity":         rule["severity"],
    }


def fuzzy_beep_from_count(count):
    memberships = fuzzify_count(count)
    label = defuzzify_max(memberships)
    rule = FUZZY_RULES_COUNT.get(label, {
        "diagnosis": "Unknown",
        "solution": "Không xác định được lỗi.",
        "severity": "unknown"
    })
    return {
        "crisp_input":      count,
        "memberships":      memberships,
        "linguistic_label": label,
        "diagnosis":        rule["diagnosis"],
        "solution":         rule["solution"],
        "severity":         rule["severity"],
        "bios_ref":         rule.get("bios_ref", ""),
    }


def fuzzy_beep(linguistic_input):
    label = linguistic_input.strip().lower() if linguistic_input else ""

    rule = FUZZY_RULES_COUNT.get(label)
    if rule:
        return {
            "linguistic_label": label,
            "diagnosis":  rule["diagnosis"],
            "solution":   rule["solution"],
            "severity":   rule["severity"],
            "bios_ref":   rule.get("bios_ref", ""),
        }

    rule = FUZZY_RULES_DURATION.get(label)
    if rule:
        return {
            "linguistic_label": label,
            "diagnosis":  rule["diagnosis"],
            "solution":   rule["solution"],
            "severity":   rule["severity"],
            "bios_ref":   "",
        }

    return {
        "linguistic_label": label,
        "diagnosis":  "Không có tiếng beep hoặc không xác định",
        "solution":   "Không cần xử lý beep code. Nếu máy không khởi động được mà không có tiếng beep, kiểm tra nguồn điện và kết nối loa trong máy tính.",
        "severity":   "normal",
        "bios_ref":   "",
    }


if __name__ == "__main__":
    print("=== Test Count-Based Rules ===")
    for label in FUZZY_RULES_COUNT:
        r = fuzzy_beep(label)
        print(f"[{label:10}] -> {r['diagnosis'][:60]}")

    print("\n=== Test Duration-Based Rules ===")
    for label in FUZZY_RULES_DURATION:
        r = fuzzy_beep(label)
        print(f"[{label:12}] -> {r['diagnosis'][:60]}")

    print("\n=== Test Crisp Duration Input ===")
    for seconds in [0.2, 0.7, 1.3, 2.2, 3.5, 5.0]:
        r = fuzzy_beep_from_crisp(seconds)
        best = r['linguistic_label']
        mu = r['memberships'][best]
        print(f"[{seconds:.1f}s] -> '{best}' (μ={mu:.2f}) -> {r['diagnosis'][:50]}")

    print("\n=== Test Crisp Count Input ===")
    for n in [1, 2, 3, 4, 5, 6, 7, 8, 10]:
        r = fuzzy_beep_from_count(n)
        best = r['linguistic_label']
        mu = r['memberships'][best]
        print(f"[{n} beep(s)] -> '{best}' (μ={mu:.2f}) -> {r['diagnosis'][:50]}")