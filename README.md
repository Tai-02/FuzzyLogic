<h1 align="center">EXPERT-SYS // Hệ Chuyên Gia Chẩn Đoán Máy Tính</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-black.svg?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1.svg?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/AI-Fuzzy%20Logic-magenta.svg" alt="Fuzzy Logic">
</p>

## 📖 Giới thiệu (Introduction)

Dự án phát triển nền tảng **Hệ chuyên gia chẩn đoán lỗi phần cứng máy tính (PC Hardware Expert System)**. Với giao diện mang phong cách **Cyberpunk UI** đậm chất viễn tưởng và kỹ thuật, hệ thống tận dụng sức mạnh trí tuệ nhân tạo thông qua kiến trúc lai (Hybrid):

1. **Suy diễn tiến (Forward Chaining):** Truy vấn qua "Cơ Sở Luật" từ hàng loạt các triệu chứng hệ thống để đưa ra quy trình sửa chữa. Sử dụng cấu trúc dữ liệu **Set** tối ưu hóa hiệu suất O(1).
2. **Logic mờ kép (Dual-Fuzzy):** Phân tích tín hiệu âm thanh POST (Beep Codes) và Nhiệt độ hệ thống (Context-Aware Temperature) thông qua thuật toán mờ, đánh giá mức độ nghiêm trọng (Severity) để cảnh báo tức thời.

---

## ✨ Tính năng nổi bật (Key Features)

- 🔍 **Thiết kế Cyberpunk Terminal:** Trải nghiệm "Hệ điều hành cảm biến" với màu nền tĩnh vật, tia quét neon, và font chữ đơn không gian chuẩn kỹ thuật.
- 🔊 **Ma trận chẩn đoán đa chiều:** Xử lý chẩn đoán song song lỗi phần cứng qua hộp thoại *Triệu chứng (Symptoms)* và *Logic mờ kép (Beeps & Temperature)*.
- 🛡️ **Motherboard X-Ray Radar:** Sơ đồ bo mạch chủ 2D tích hợp hiệu ứng tia quét Laser (`Laser Scan`) với khả năng báo lỗi đỏ rực tại vị trí linh kiện bị lỗi.
- ⚙️ **Core Knowledge Base Terminal:** Trạm Quản trị (`/admin`) được thiết kế bảo mật để nạp liệu và tháo gỡ Luật IF-THEN trong thời gian thực.

---

## 📂 Kiến trúc hệ thống (Repository)

```text
FuzzyLogic/
├── app.py              # Main Flask Engine // Route & Logic Điều Khiển
├── fuzzy.py            # AI Module // Không gian Logic Mờ & Thuật toán thành viên
├── data.sql            # Core Data // Chứa Database Schema chứa Core Rules
├── docker-compose.yml  # Container Orchestration // Tự động ảo hóa môi trường
├── Dockerfile          # Image Builder // Config Python Worker
├── static/             # Assets tĩnh
│   └── style.css       # Design System // Hệ thống UI Cyberpunk & Animation Laser
└── templates/          # Jinja2 Layouts
    ├── index.html      # Trạm điều khiển chẩn đoán (Diagnostic Terminal)
    ├── result.html     # Kết quả suy diễn với Sơ đồ X-Ray (Result Radar)
    └── admin.html      # Trạm nạp tri thức gốc (Core_KB)
```

---

## ⚙️ Trạm Quản Trị & Bảo Mật (Admin & Security)

Hệ thống đã được tích hợp lớp bảo mật để bảo vệ cơ sở dữ liệu tri thức.
- **Đường dẫn truy cập:** `http://localhost:5000/admin`
- **Tài khoản mặc định:**
  - **Username:** `admin`
  - **Password:** `admin123`
- **Cơ chế:** Mật khẩu được mã hóa chuẩn **scrypt** trong cơ sở dữ liệu thông qua `werkzeug.security`.

---

## 🚀 Khởi chạy & Thiết lập (Installation)

### 🐳 Cách 1: Sử dụng Docker (Khuyên dùng)
1. **Khởi động:**
   ```powershell
   docker-compose up -d --build
   ```
2. **Cập nhật Database (Nếu bạn sửa file data.sql):**
   Chạy lệnh sau trong PowerShell để nạp lại dữ liệu mà không cần restart container:
   ```powershell
   Get-Content data.sql | docker exec -i fuzzy_db mysql -u root -proot_password expert_system
   ```

### 🐍 Cách 2: Chạy thủ công (Manual)
1. Cài đặt thư viện: `pip install flask mysql-connector-python werkzeug`
2. Tạo database `expert_system` trong MySQL và Import file `data.sql`.
3. Chạy: `python app.py`

---

## 🧰 Kịch bản vận hành (Operation Protocol)

### 1. Chẩn đoán lỗi (User Terminal)
- Chọn các triệu chứng thực tế của máy tính.
- Kéo thanh nhiệt độ để AI phân tích theo ngữ cảnh (Office/Gaming).
- Nhấn **KHỞI ĐỘNG CHẨN ĐOÁN** để chạy Laser Scan và xem sơ đồ X-Ray.

### 2. Quản lý tri thức (Knowledge Base)
- Đăng nhập vào `/admin` để thêm luật. 
- **Quy tắc nhập:** Các điều kiện cách nhau bằng dấu phẩy (Ví dụ: `CPU, Nóng, Loud fan noise`). Hệ thống sẽ tự động gộp các triệu chứng này vào danh mục tương ứng ở trang chủ.

---

## 📚 Cơ sở khoa học (Scientific References)

1.  **Youssef Bassil (2012):** *"Expert PC Troubleshooter With Fuzzy-Logic and Self-Learning Support"*, IJCS Issue 1.
2.  **MDPI Applied Sciences:** *"Application of Fuzzy Logic for Problems of Evaluating States of a Computing System"*.
3.  **P. Singhala et al. (2014):** *"Temperature Control using Fuzzy Logic"*, Arxiv.

---

## 👥 Nhóm thực hiện (Group 8)

- **Nguyễn Minh Đại:** UI/UX Design & X-Ray Radar System.
- **Trần Quốc Tài:** AI Logic Architecture & Dual-Fuzzy Algorithms.
- **Bùi Minh Tân:** Backend Engine & Database Management.

---
*> // PHẦN MỀM THUỘC SỞ HỮU TRÍ TUỆ ĐỒ ÁN MÔN HỌC HỆ CHUYÊN GIA — CÔNG NGHỆ FLASK & FUZZY AI //*
