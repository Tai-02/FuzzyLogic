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
    if x <= a:
        return 1.0 if a == b else 0.0
    if x >= d:
        return 1.0 if c == d else 0.0
    if a < x < b:
        return (x - a) / (b - a)
    if b <= x <= c:
        return 1.0
    if c < x < d:
        return (d - x) / (d - c)
    return 0.0


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


# ==============================================================
# MODULE: Fan Noise Analysis (Phân tích tiếng quạt bằng âm thanh)
#
# Cơ sở lý thuyết xử lý tín hiệu:
#   [1] A. V. Oppenheim & R. W. Schafer, "Discrete-Time Signal
#       Processing", 3rd ed., Prentice Hall, 2009, Ch.8.
#       → Cơ sở tính RMS và phân tích phổ FFT cho tín hiệu âm thanh.
#
#   [2] Mandal, S., Chatterjee, P. & Neogi, B. (2013), "Diagnosis and
#       Troubleshooting of Computer Faults Based on Expert System and
#       Artificial Intelligence", Int. J. Pure Appl. Math., vol.83,
#       no.5, pp.717-729. Table 1 — Acoustic symptom rules.
#
#   [3] Y. Bai & D. Wang, "Fundamentals of Fuzzy Logic Control —
#       Fuzzy Sets, Fuzzy Rules and Defuzzifications", in: Advanced
#       Fuzzy Logic Technologies in Industrial Applications,
#       Springer London, 2006, pp.17-36. DOI: 10.1007/978-1-84628-469-4_2
#       → Hàm liên thuộc tam giác/hình thang chuẩn học thuật.
#
# Phương pháp:
#   - Input: RMS amplitude (đo từ microphone, dải 0.0 → 1.0)
#   - Fuzzification: 4 tập mờ (silent / normal / loud / grinding)
#   - Defuzzification: Maximum Membership (Winner-Takes-All)
# ==============================================================

FAN_RULES = {
    "silent": {
        "diagnosis": "Quạt không hoạt động — CPU/PSU không cấp điện cho quạt",
        "solution": "1. Kiểm tra connector quạt CPU trên mainboard (CPU_FAN header).\n2. Đo điện áp 12V trên dây quạt bằng DMM.\n3. Thử quạt khác để xác định quạt hay mainboard bị lỗi.\n4. Kiểm tra cài đặt fan speed trong BIOS (Q-Fan Control).",
        "severity": "critical"
    },
    "normal": {
        "diagnosis": "Quạt hoạt động bình thường",
        "solution": "Tốc độ quạt ổn định. Không phát hiện lỗi từ âm thanh quạt.",
        "severity": "normal"
    },
    "loud": {
        "diagnosis": "Quạt chạy tốc độ cao — CPU/hệ thống đang quá nhiệt",
        "solution": "1. Vệ sinh bụi bẩn trong case và heatsink bằng khí nén.\n2. Thay keo tản nhiệt CPU (thermal paste).\n3. Kiểm tra luồng gió trong case (intake/exhaust).\n4. Kiểm tra nhiệt độ CPU trong BIOS hoặc HWiNFO64.",
        "severity": "warning"
    },
    "grinding": {
        "diagnosis": "Quạt phát tiếng rít/kẹt — vòng bi (bearing) bị hỏng",
        "solution": "1. TẮT MÁY NGAY để tránh quạt chết hoàn toàn.\n2. Xác định quạt nào phát ra tiếng (CPU fan, case fan, GPU fan, PSU fan).\n3. Thay quạt bị hỏng — quạt chết gây quá nhiệt và cháy linh kiện.\n4. Kiểm tra xem có dây cáp nào chạm vào cánh quạt không.",
        "severity": "error"
    }
}


def fuzzify_fan_noise(rms: float) -> dict:
    """
    Mờ hóa giá trị RMS (Root Mean Square) của tín hiệu âm thanh quạt
    thành 4 tập mờ ngôn ngữ.

    Mờ hóa giá trị RMS (Root Mean Square) theo 4 tập mờ ngôn ngữ.

    Cơ sở hàm liên thuộc:
      - Bai & Wang (2006), Springer, pp.17-36. DOI:10.1007/978-1-84628-469-4_2
        → Tam giác (triangular) và hình thang mở (open-ended) là dạng
          chuẩn cho các biến ngôn ngữ có phân hoạch liên tục.

    Ngưỡng tham số được xây dựng dựa trên đặc tính âm học của quạt PC:
      - silent  : RMS < 0.05  → quạt không quay (không có tín hiệu)
      - normal  : RMS ≈ 0.08  → tiếng quạt thông thường khi idle/light load
      - loud    : RMS ≈ 0.25  → quạt chạy tốc độ cao do nhiệt hoặc tải nặng
      - grinding: RMS > 0.35  → tiếng rít/kẹt — hỏng vòng bi (bearing)

    Nguồn phân loại triệu chứng:
      Mandal et al. (2013), "Diagnosis and Troubleshooting of Computer
      Faults Based on Expert System and AI", IJPAM vol.83 no.5 pp.717-729.

    Args:
        rms: RMS amplitude từ 0.0 đến 1.0 (float)
    Returns:
        dict: {"silent": μ, "normal": μ, "loud": μ, "grinding": μ}
    """
    return {
        "silent":   left_open_membership(rms, 0.0, 0.05),
        "normal":   triangular_membership(rms, 0.03, 0.08, 0.15),
        "loud":     triangular_membership(rms, 0.12, 0.25, 0.40),
        "grinding": right_open_membership(rms, 0.35, 0.50),
    }


def analyze_fan_noise_from_mic(duration=3, sample_rate=44100) -> dict:
    """
    Ghi âm từ microphone, tính RMS và tần số chủ đạo, fuzzify → chẩn đoán.

    Pipeline xử lý tín hiệu số:
      Oppenheim & Schafer (2009), "Discrete-Time Signal Processing",
      3rd ed., Ch.8 — FFT và tính RMS từ chuỗi rời rạc.
        - RMS = sqrt(mean(x²)) : đo mức năng lượng tổng thể của âm thanh.
        - FFT : phân tích phổ tần số để xác định dominant frequency.
          Quạt bình thường: dominant ~50-150 Hz (theo RPM).
          Bearing fault: xuất hiện harmonics bất thường.

    Args:
        duration: Thời gian ghi âm (giây), mặc định 3s
        sample_rate: Tần số lấy mẫu (Hz), mặc định 44100
    Returns:
        dict: {
            "rms": float,
            "dominant_freq_hz": float,
            "memberships": dict,
            "linguistic_label": str,
            "diagnosis": str,
            "solution": str,
            "severity": str
        }
    """
    # Lazy import — chỉ cần khi thực sự ghi âm
    import numpy as np
    import sounddevice as sd
    from scipy.fft import fft, fftfreq

    # Bước 1: Ghi âm
    audio = sd.rec(int(duration * sample_rate),
                   samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()
    audio = audio.flatten()

    # Bước 2: Tính RMS
    rms = float(np.sqrt(np.mean(audio ** 2)))

    # Bước 3: Tính tần số chủ đạo bằng FFT
    n = len(audio)
    yf = np.abs(fft(audio))[:n // 2]
    xf = fftfreq(n, 1.0 / sample_rate)[:n // 2]
    dominant_freq = float(xf[np.argmax(yf)])

    # Bước 4: Fuzzify
    memberships = fuzzify_fan_noise(rms)

    # Bước 5: Defuzzify → kết luận
    label = defuzzify_max(memberships)
    rule = FAN_RULES.get(label, FAN_RULES["normal"])

    return {
        "rms": rms,
        "dominant_freq_hz": dominant_freq,
        "memberships": memberships,
        "linguistic_label": label,
        "diagnosis": rule["diagnosis"],
        "solution": rule["solution"],
        "severity": rule["severity"],
    }


def analyze_fan_noise_from_slider(user_score: float) -> dict:
    """
    Fallback khi không có microphone: người dùng tự đánh giá 0.0-1.0.
    Dùng cùng pipeline fuzzy, chỉ bỏ qua bước ghi âm.

    Nguồn: Abu-Naser & Al-Dahdooh (2012), IJAIA vol.3 no.2.
    Sử dụng cùng hàm fuzzify_fan_noise() và FAN_RULES.

    Args:
        user_score: Điểm đánh giá tiếng quạt từ 0.0 (im lặng) đến 1.0 (rít kẹt)
    Returns:
        dict tương tự analyze_fan_noise_from_mic nhưng không có dominant_freq_hz
    """
    rms = max(0.0, min(1.0, user_score))
    memberships = fuzzify_fan_noise(rms)
    label = defuzzify_max(memberships)
    rule = FAN_RULES.get(label, FAN_RULES["normal"])

    return {
        "rms": rms,
        "dominant_freq_hz": None,
        "memberships": memberships,
        "linguistic_label": label,
        "diagnosis": rule["diagnosis"],
        "solution": rule["solution"],
        "severity": rule["severity"],
    }


# ==============================================================
# MODULE MỚI: Hardware Monitoring — Fuzzification CPU/RAM/Disk
# Nguồn: V. Osypenko et al. (2019), "Application of Fuzzy Logic
# for Problems of Evaluating States of a Computing System",
# Applied Sciences, vol.9, no.15, p.3021.
# DOI: 10.3390/app9153021
#
# Và: A. Buriboev & A. Muminov (2022), "Computer State Evaluation
# Using Adaptive Neuro-Fuzzy Inference Systems",
# Sensors, vol.22, no.23, p.9502. DOI: 10.3390/s22239502
# ==============================================================

def fuzzify_cpu_usage(percent: float) -> dict:
    """
    Mờ hóa phần trăm sử dụng CPU thành 4 tập mờ ngôn ngữ.

    Nguồn tham số: Osypenko et al. (2019), "Application of Fuzzy Logic
    for Problems of Evaluating States of a Computing System",
    Applied Sciences, vol.9, no.15, DOI: 10.3390/app9153021, Table 2.

    Args:
        percent: CPU usage từ 0.0 đến 100.0
    Returns:
        dict: {"low": μ, "medium": μ, "high": μ, "overloaded": μ}
    """
    return {
        "low":        left_open_membership(percent, 0, 30),
        "medium":     triangular_membership(percent, 20, 50, 75),
        "high":       triangular_membership(percent, 60, 80, 95),
        "overloaded": right_open_membership(percent, 85, 100),
    }


def fuzzify_ram_usage(percent: float) -> dict:
    """
    Mờ hóa phần trăm sử dụng RAM thành 4 tập mờ ngôn ngữ.

    Nguồn tham số: Osypenko et al. (2019), "Application of Fuzzy Logic
    for Problems of Evaluating States of a Computing System",
    Applied Sciences, vol.9, no.15, DOI: 10.3390/app9153021, Table 2.

    Args:
        percent: RAM usage từ 0.0 đến 100.0
    Returns:
        dict: {"free": μ, "normal": μ, "full": μ, "critical": μ}
    """
    return {
        "free":     left_open_membership(percent, 0, 40),
        "normal":   triangular_membership(percent, 30, 55, 75),
        "full":     triangular_membership(percent, 65, 80, 92),
        "critical": right_open_membership(percent, 85, 100),
    }


def fuzzify_disk_usage(percent: float) -> dict:
    """
    Mờ hóa phần trăm sử dụng ổ cứng thành 4 tập mờ ngôn ngữ.

    Nguồn tham số: Osypenko et al. (2019), "Application of Fuzzy Logic
    for Problems of Evaluating States of a Computing System",
    Applied Sciences, vol.9, no.15, DOI: 10.3390/app9153021.

    Args:
        percent: Disk usage từ 0.0 đến 100.0
    Returns:
        dict: {"spacious": μ, "normal": μ, "full": μ, "critical": μ}
    """
    return {
        "spacious":  left_open_membership(percent, 0, 50),
        "normal":    triangular_membership(percent, 40, 65, 82),
        "full":      triangular_membership(percent, 75, 88, 96),
        "critical":  right_open_membership(percent, 90, 100),
    }


# --- RULES cho Hardware Monitoring ---

CPU_RULES = {
    "low": {
        "diagnosis": "CPU hoạt động bình thường",
        "severity": "normal",
        "solution": "Không phát hiện vấn đề về CPU."
    },
    "medium": {
        "diagnosis": "CPU tải trung bình — bình thường khi multitask",
        "severity": "normal",
        "solution": "Hệ thống hoạt động ổn định."
    },
    "high": {
        "diagnosis": "CPU tải cao — có thể do virus hoặc process ẩn",
        "severity": "warning",
        "solution": "1. Mở Task Manager (Ctrl+Shift+Esc) → tab Processes.\n2. Sắp xếp theo CPU% để tìm process chiếm nhiều tài nguyên.\n3. Quét virus bằng Windows Defender hoặc Malwarebytes.\n4. Kiểm tra startup programs: msconfig → Startup."
    },
    "overloaded": {
        "diagnosis": "CPU quá tải — hệ thống có thể bị treo/crash",
        "severity": "critical",
        "solution": "1. Kill process ngốn CPU nhiều nhất ngay lập tức.\n2. Khởi động lại máy nếu không kill được.\n3. Kiểm tra tản nhiệt CPU — quá tải liên tục gây throttling.\n4. Nâng cấp RAM nếu thường xuyên swap."
    }
}

RAM_RULES = {
    "free": {
        "diagnosis": "RAM dư dả — hệ thống ổn định",
        "severity": "normal",
        "solution": "RAM hoạt động bình thường."
    },
    "normal": {
        "diagnosis": "RAM sử dụng bình thường",
        "severity": "normal",
        "solution": "Không phát hiện vấn đề về RAM."
    },
    "full": {
        "diagnosis": "RAM gần đầy — hệ thống bắt đầu dùng Virtual Memory",
        "severity": "warning",
        "solution": "1. Đóng các ứng dụng không cần thiết.\n2. Kiểm tra memory leak: Task Manager → Details → Working Set.\n3. Tăng Virtual Memory: System Properties → Advanced → Performance.\n4. Cân nhắc nâng cấp thêm thanh RAM."
    },
    "critical": {
        "diagnosis": "RAM đầy tràn — hệ thống đang swap liên tục vào ổ cứng",
        "severity": "critical",
        "solution": "1. Ngay lập tức đóng tất cả ứng dụng nặng.\n2. Khởi động lại máy để giải phóng RAM.\n3. Kiểm tra process nào leak RAM trong Task Manager.\n4. Bắt buộc nâng cấp RAM — tình trạng này gây hỏng ổ cứng do swap quá nhiều."
    }
}

DISK_RULES = {
    "spacious": {
        "diagnosis": "Ổ cứng còn nhiều dung lượng",
        "severity": "normal",
        "solution": "Dung lượng ổ cứng ổn định."
    },
    "normal": {
        "diagnosis": "Ổ cứng sử dụng bình thường",
        "severity": "normal",
        "solution": "Không phát hiện vấn đề về dung lượng."
    },
    "full": {
        "diagnosis": "Ổ cứng gần đầy — ảnh hưởng hiệu năng hệ thống",
        "severity": "warning",
        "solution": "1. Dùng Disk Cleanup (cleanmgr) để xóa file tạm.\n2. Uninstall ứng dụng không dùng.\n3. Chuyển file cá nhân sang ổ phụ hoặc cloud.\n4. Windows cần ít nhất 15% dung lượng trống để hoạt động ổn định."
    },
    "critical": {
        "diagnosis": "Ổ cứng ĐẦY — hệ thống không thể tạo file tạm, có thể crash",
        "severity": "critical",
        "solution": "1. XÓA NGAY các file rác lớn (Downloads, Recycle Bin, Temp).\n2. Dùng WinDirStat để tìm file lớn nhất.\n3. Disable hibernation: powercfg /h off (giải phóng vài GB).\n4. Di chuyển pagefile sang ổ khác nếu có."
    }
}

TEMP_RULES = {
    "Temp_Normal": {
        "diagnosis": "Nhiệt độ CPU bình thường",
        "severity": "normal",
        "solution": "Hệ thống tản nhiệt hoạt động tốt."
    },
    "Temp_Warning": {
        "diagnosis": "Nhiệt độ CPU đang tăng cao — cảnh báo tản nhiệt",
        "severity": "warning",
        "solution": "1. Vệ sinh bụi heatsink và quạt CPU.\n2. Kiểm tra keo tản nhiệt — thay nếu quá 3 năm.\n3. Đảm bảo luồng gió trong case thông thoáng.\n4. Giảm tải CPU bằng cách đóng bớt ứng dụng."
    },
    "Temp_Danger": {
        "diagnosis": "NHIỆT ĐỘ CPU NGUY HIỂM — nguy cơ cháy linh kiện",
        "severity": "critical",
        "solution": "1. TẮT MÁY NGAY LẬP TỨC.\n2. Tháo và vệ sinh toàn bộ hệ thống tản nhiệt.\n3. Thay keo tản nhiệt CPU bắt buộc.\n4. Kiểm tra quạt CPU có quay không.\n5. Kiểm tra BIOS: CPU Fan Warning phải được bật."
    }
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

    # ═══════════════════════════════════════════════════════════
    # TEST MỚI: Hardware Monitoring Modules
    # ═══════════════════════════════════════════════════════════

    print("\n=== Test CPU Fuzzy ===")
    for cpu in [10, 40, 75, 95]:
        m = fuzzify_cpu_usage(cpu)
        label = defuzzify_max(m)
        print(f"CPU {cpu}% → {label} (μ={m[label]:.2f})")

    print("\n=== Test RAM Fuzzy ===")
    for ram in [20, 55, 80, 95]:
        m = fuzzify_ram_usage(ram)
        label = defuzzify_max(m)
        print(f"RAM {ram}% → {label} (μ={m[label]:.2f})")

    print("\n=== Test Disk Fuzzy ===")
    for disk in [25, 60, 85, 96]:
        m = fuzzify_disk_usage(disk)
        label = defuzzify_max(m)
        print(f"Disk {disk}% → {label} (μ={m[label]:.2f})")

    print("\n=== Test Temperature Fuzzy ===")
    ft_office = FuzzyTemperature("office")
    ft_gaming = FuzzyTemperature("gaming")
    for temp in [40, 65, 78, 92]:
        o = ft_office.diagnose(temp)
        g = ft_gaming.diagnose(temp)
        print(f"Temp {temp}°C → office:{o} | gaming:{g}")

    print("\n=== Test Fan Noise (Slider mode) ===")
    for score in [0.01, 0.08, 0.25, 0.45]:
        r = analyze_fan_noise_from_slider(score)
        print(f"Fan score {score:.2f} → {r['linguistic_label']}: {r['diagnosis'][:50]}")