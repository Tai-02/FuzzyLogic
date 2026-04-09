<h1 align="center">PC Hardware Expert System with Fuzzy Logic 💻</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black.svg?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1.svg?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/AI-Fuzzy%20Logic-magenta.svg" alt="Fuzzy Logic">
</p>

## 📖 Giới thiệu (Introduction)

Dự án này là một **Hệ chuyên gia chẩn đoán lỗi phần cứng máy tính (Expert System for Hardware Diagnosis)**, kết hợp giữa hai phương pháp:
1. **Suy diễn tiến (Forward Chaining):** Dựa trên các triệu chứng được người dùng lựa chọn để đưa ra nguyên nhân và cách khắc phục.
2. **Logic mờ (Fuzzy Logic):** Xử lý và phân tích các mã âm thanh bíp (Beep Codes) từ Mainboard (dựa trên số lượng bíp hoặc độ dài của bíp) để đưa ra chẩn đoán chính xác về trạng thái của hệ thống POST.

---

## ✨ Tính năng nổi bật (Key Features)

- 🔍 **Chẩn đoán theo triệu chứng:** Chọn nhiều triệu chứng mắc phải (VD: màn hình xanh, quạt quay nhưng không lên hình...) để hệ thống lọc ra lỗi.
- 🔊 **Phân tích Beep Code với Fuzzy Logic:** Phân loại và chẩn đoán lỗi phần cứng dựa trên tiếng bíp của BIOS (từ 1 đến 9+ tiếng bíp, hoặc tiếng bíp ngắn/dài/liên tục).
- 🛠️ **Giao diện quản trị (Admin Panel):** Cho phép Quản trị viên dễ dàng thêm mới, sửa đổi hoặc xóa bỏ các Luật (Rules) trực tiếp trên giao diện web (`/admin`).
- ⚡ **Giao diện Web thân thiện:** Được xây dựng nhanh chóng bằng Flask và dễ dàng sử dụng trên trình duyệt.

---

## 📂 Cấu trúc thư mục (Project Structure)

```text
FuzzyLogic/
├── app.py              # File chạy server Flask chính, chứa logic route và kết nối DB.
├── fuzzy.py            # Chứa các thuật toán tập mờ (Membership functions) & Luật mờ (Fuzzy Rules).
├── data.sql            # File script khôi phục cơ sở dữ liệu MySQL định dạng các luật.
├── static/             # Thư mục chứa tài nguyên tĩnh: CSS, JavaScript, Hình ảnh,...
├── templates/          # Thư mục giao diện HTML:
│   ├── index.html      # Trang chủ (chọn triệu chứng).
│   ├── result.html     # Kết quả chẩn đoán.
│   └── admin.html      # Trang quản lý các quy tắc luật.
└── README.md           # Tài liệu hướng dẫn này.
```

---

## 🚀 Cài đặt và Chạy thử (Installation & Setup)

### Yêu cầu hệ thống (Prerequisites)
- [Python 3.8+](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/installer/) (hoặc XAMPP/WAMP)
- Virtual Environment (Tuỳ chọn nhưng khuyến khích)

### Các bước thực hiện

**Bước 1: Clone/Tải dự án về máy**
Di chuyển file project vào một thư mục, ví dụ `d:\source code\FuzzyLogic`.

**Bước 2: Cài đặt thư viện Python**
Mở terminal/cmd tại thư mục dự án và chạy:
```bash
pip install flask mysql-connector-python
```

**Bước 3: Thiết lập cơ sở dữ liệu**
1. Mở MySQL/phpMyAdmin lên.
2. Tạo một database mới tên là: `expert_system`.
3. Import file `data.sql` có sẵn trong thư mục để tạo bảng `rules` và các dữ liệu mẫu.
4. *Lưu ý:* Mở file `app.py` (dòng 7-12) và sửa thông tin đăng nhập MySQL nếu máy bạn dùng password khác (mặc định trong code đang là user `root`, password `0866582512`).

**Bước 4: Khởi chạy ứng dụng**
Tại terminal trong thư mục `FuzzyLogic`, chạy lệnh sau để khởi động server:
```bash
python app.py
```
Ứng dụng sẽ chạy tại địa chỉ: `http://localhost:5000` hoặc `http://127.0.0.1:5000`.

---

## 🧰 Hướng dẫn sử dụng (Usage)

- **Trang chủ (`/`):** Tích chọn các triệu chứng phần cứng mà bạn đang gặp phải, có thể chọn kèm tiếng Beep của BIOS, sau đó nhấn "Chẩn đoán".
- **Trang quản trị (`/admin`):** Khu vực để thêm luật IF-THEN mới cho hệ chuyên gia.

---
*Phát triển cho mục đích học tập và nghiên cứu AI - Hệ chuyên gia (Expert Systems) & Logic mờ (Fuzzy Logic).*
