<h1 align="center">EXPERT-SYS // Hệ Chuyên Gia Chẩn Đoán Lỗi Phần Cứng</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue.svg?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-black.svg?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1.svg?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/AI-Fuzzy%20Logic-magenta.svg" alt="Fuzzy Logic">
</p>

## 📖 Giới thiệu (Introduction)

Đây là **Hệ chuyên gia chẩn đoán lỗi phần cứng máy tính** tích hợp Trí tuệ nhân tạo (Logic mờ - Fuzzy Logic). Hệ thống sử dụng kiến trúc phân tán gồm Server (Web/Database) và Local Agent (để đo cảm biến và ghi âm trên máy khách).

Hệ thống có 2 khả năng chẩn đoán chính:
1. **Chẩn đoán khi máy KHÔNG boot được (Acoustic Diagnosis):** Ghi âm trực tiếp Tiếng Bíp BIOS và Tiếng Quạt để phân tích mờ (Fuzzification).
2. **Chẩn đoán khi máy còn màn hình (Hardware Scan):** Quét thông số CPU, RAM, Ổ cứng, Nhiệt độ thực tế để đánh giá "sức khỏe" hệ thống.

---

## 🚀 Hướng dẫn chạy đồ án (Dành cho người kiểm thử)

Hệ thống được thiết kế theo kiến trúc **Agent-Client**. Để trải nghiệm đầy đủ, bạn chỉ cần làm theo 2 bước sau:

### Bước 1: Khởi động Server (Web & Database)
1. Cài đặt Docker Desktop.
2. Mở Terminal tại thư mục code và chạy lệnh:
   ```powershell
   docker-compose up -d
   ```
3. Truy cập Web tại: **`http://localhost:5000`**

### Bước 2: Khởi động Cảm biến (Ghi âm & Nhiệt độ thật)
Để sử dụng được nút **[🎙 Ghi âm]** và đo được **Nhiệt độ thật**, bạn cần chạy Agent trên Windows:
1. Nhấn đúp chuột (Double-click) vào file **`CHAY_NHANH.bat`** trong thư mục.
2. Hệ thống sẽ tự động hoạt động ở 2 chế độ:
   - **Chế độ Real-time:** Nếu bạn mở **LibreHardwareMonitor** (quyền Admin), Agent sẽ lấy nhiệt độ CPU thật qua giao thức WMI.
   - **Chế độ Simulation:** Nếu không mở phần mềm bổ trợ, Agent sẽ tự động nội suy nhiệt độ dựa trên tải (load) của CPU để đảm bảo dữ liệu Demo luôn sống động.
3. Quay lại trình duyệt và tận hưởng giao diện chẩn đoán Cyberpunk!

---

## 🛠️ Kiến trúc Kỹ thuật (Technical Architecture)
Hệ thống này tích hợp các kỹ thuật tiên tiến để tối ưu cho việc chẩn đoán:
- **Acoustic Diagnostic:** Sử dụng Fast Fourier Transform (FFT) và tính toán RMS để phân tích âm thanh tiếng bíp BIOS và tiếng quạt.
- **Fuzzy Inference Engine:** Xử lý các giá trị mờ (Low, Normal, Danger) thay vì các con số cứng nhắc.
- **Dual-Mode Thermal Sensing:** Khả năng giao tiếp với tầng Kernel của Windows thông qua WMI (Windows Management Instrumentation) và Namespace `root\LibreHardwareMonitor`.

Để thêm hoặc sửa các luật (Rules) của hệ chuyên gia:
- **Đường dẫn truy cập:** `http://localhost:5000/admin`
- **Tài khoản mặc định:**
  - **Username:** `admin`
  - **Password:** `admin123`
- Lưu ý: Các luật được kết nối bằng Suy diễn tiến (Forward Chaining).

---

## 📚 Cơ sở khoa học (Scientific References)

Hệ thống được lập trình bám sát các nghiên cứu chuẩn học thuật:
1.  **Tiếng Bíp BIOS:** S. S. Abu-Naser & R. Al-Dahdooh (2012), *"Expert PC Troubleshooter With Fuzzy-Logic"*, IJAIA vol.3.
2.  **Tiếng Quạt & Xử lý âm thanh (RMS/FFT):** 
    - A. V. Oppenheim & R. W. Schafer (2009), *"Discrete-Time Signal Processing"*.
    - Mandal et al. (2013), *"Diagnosis and Troubleshooting of Computer Faults Based on Expert System and AI"*.
3.  **Hàm liên thuộc mờ:** Y. Bai & D. Wang (2006), *"Fundamentals of Fuzzy Logic Control"*, Springer.
4.  **Đánh giá Phần cứng (CPU/RAM/Temp):** V. Osypenko et al. (2019) và A. Buriboev et al. (2022) ứng dụng Hệ suy diễn Neuro-Fuzzy trên Sensors & Applied Sciences.

---

## 👥 Nhóm thực hiện (Group 8)

- **Nguyễn Minh Đại:** UI/UX Design & X-Ray Radar System.
- **Trần Quốc Tài:** AI Logic Architecture & Dual-Fuzzy Algorithms.
- **Bùi Minh Tân:** Backend Engine & Database Management.
