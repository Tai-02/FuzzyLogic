<h1 align="center">EXPERT-SYS // Hệ Chuyên Gia Chẩn Đoán Máy Tính</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-black.svg?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1.svg?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/AI-Fuzzy%20Logic-magenta.svg" alt="Fuzzy Logic">
</p>

## 📖 Giới thiệu (Introduction)

Dự án phát triển nền tảng **Hệ chuyên gia chẩn đoán lỗi phần cứng máy tính (PC Hardware Expert System)**. Với giao diện mang phong cách **Cyberpunk UI** đậm chất viễn tưởng và kỹ thuật, hệ thống tận dụng sức mạnh trí tuệ nhân tạo thông qua:
1. **Suy diễn tiến (Forward Chaining):** Truy vấn qua "Cơ Sở Luật" từ hàng loạt các triệu chứng hệ thống để khoanh vùng nguyên nhân và đưa ra quy trình sửa chữa.
2. **Logic mờ (Fuzzy Logic):** Phân tích tín hiệu âm thanh POST (Beep Codes) từ BIOS thông qua thuật toán mờ, đánh giá mức độ nghiêm trọng (Severity) để cảnh báo tức thời.

---

## ✨ Tính năng nổi bật (Key Features)

- 🔍 **Thiết kế Cyberpunk Terminal:** Trải nghiệm "Hệ điều hành cảm biến" với màu nền tĩnh vật, tia quét neon, và font chữ đơn không gian chuẩn kỹ thuật.
- 🔊 **Ma trận chẩn đoán đa chiều:** Xử lý chẩn đoán song song lỗi phần cứng qua hộp thoại *Triệu chứng (Symptoms)* và *Tần số mờ tiếng Bíp (Fuzzy Beeps)*.
- 🛡️ **Motherboard X-Ray Radar:** Sơ đồ bo mạch chủ 2D tích hợp hiệu ứng tia quét Laser (`Laser Scan`) với khả năng bắt tín hiệu cảnh báo màu đỏ chói khi có linh kiện phát sinh lỗi chẩn đoán.
- ⚙️ **Core Knowledge Base Terminal:** Trạm Quản trị (`/admin`) được thiết kế bảo mật để nhập liệu và tháo gỡ Luật IF-THEN trong thời gian thực.
- 🐳 **Triển khai 1 giây với Docker:** Đóng gói hoàn chỉnh Database và Server, sẵn sàng ảo hóa trên mọi thiết bị chấm đồ án.

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

## 🚀 Khởi chạy hệ thống nghiệm thu (Quick Start)

Dự án này đã được đóng gói toàn diện bằng Docker để đơn giản hóa quá trình chạy đồ án. Tránh xung đột môi trường Python 100%.

### Cách 1: Khởi động siêu tốc bằng Docker (Khuyên dùng 🌟)
*Yêu cầu môi trường đã cài đặt Docker Desktop.*

1. Mở Terminal / PowerShell tại thư mục đồ án:
   ```bash
   cd "d:\source code\FuzzyLogic"
   ```
2. Kéo hệ thống Online bằng lệnh cơ bản:
   ```bash
   docker-compose up -d --build
   ```
3. Sau 30s hệ cơ sở dữ liệu khởi tạo xong, truy cập bằng trình duyệt web:
   👉 **http://localhost:5000**

*Lưu ý: Bạn có thể sửa trực tiếp HTML/CSS, Web sẽ tự nhận lệnh mà không cần tắt Docker.*

### Cách 2: Khởi chạy môi trường thuần (Manual)
*Yêu cầu: Đã cài Local MySQL server và Python 3.8+*

1. Đổ dữ liệu file `data.sql` vào MySQL Database (Tên DB: `expert_system`).
2. Sửa Pass DB nội bộ tại 4 biến môi trường đầu chuỗi nằm ở đoạn `app.py`.
3. Tải các package liên kết: `pip install flask mysql-connector-python`
4. Lên sóng máy chủ: `python app.py`

---

## 🧰 Kịch bản sử dụng (Operation Protocol)

- **Trạm chẩn đoán (`/`):** Bật các nút gạt chẩn đoán (Toggles), chọn tín hiệu âm thanh thu được, bấm lệnh `[ KHỞI ĐỘNG CHẨN ĐOÁN ]` và xem Radar tia Laser quét X-Ray hoạt động.
- **Trạm nạp lượng tử (`/admin`):** Thêm các dòng "Điều Kiện", "Kết Luận" ngăn cách nhau qua dấu phẩy (,) rồi nạp vào Database.

---
*> // PHẦN MỀM THUỘC SỞ HỮU TRÍ TUỆ ĐỒ ÁN MÔN HỌC HỆ CHUYÊN GIA — CÔNG NGHỆ FLASK & FUZZY AI //*
