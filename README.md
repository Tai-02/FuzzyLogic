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

Hệ thống được thiết kế theo kiến trúc **Agent-Client**. Máy chủ Web/DB chạy trong Docker, còn Cảm biến (Hardware Agent) chạy để thu thập dữ liệu. Có 2 cách chạy tùy thuộc vào nhu cầu báo cáo của bạn:

### 🌟 Kịch bản 1: Chỉ trải nghiệm Giao diện & Logic mờ (Dễ nhất)
*Phù hợp nếu bạn chỉ muốn xem giao diện, kéo các thanh trượt (sliders) giả lập thông số để xem thuật toán suy luận mờ hoạt động ra sao.*

1. Cài đặt Docker Desktop.
2. Mở Terminal (PowerShell) tại thư mục chứa code và chạy lệnh:
   ```powershell
   docker-compose up -d
   ```
3. Chờ khởi động xong, truy cập: **`http://localhost:5000`**.
*(Lưu ý: Chạy kiểu này hệ thống sẽ tự dùng Agent ảo trong Docker. Chức năng [Ghi âm Mic] sẽ bị lỗi vì Docker không có quyền truy cập Microphone của máy tính thật).*

### 🔥 Kịch bản 2: Báo cáo tính năng Ghi âm & Đo cấu hình thật (Dành cho Demo Hội đồng)
*Bắt buộc phải chạy Local Agent trên Windows để hệ thống có quyền truy cập vào Microphone và lấy chính xác phần trăm CPU/RAM của máy thật.*

1. Vẫn giữ Docker chạy bằng lệnh `docker-compose up -d` (Để chạy Web và Database).
2. Mở một cửa sổ Terminal (PowerShell) **MỚI**.
3. Cài đặt thư viện Python (Chỉ cần làm lần đầu):
   ```powershell
   pip install flask flask-cors psutil sounddevice numpy scipy
   ```
4. Chạy Agent thu thập dữ liệu phần cứng:
   ```powershell
   python hardware_agent.py
   ```
*(Kệ thông báo Warning đỏ của Flask, cứ để cửa sổ đó chạy ngầm. Bây giờ bạn truy cập Web và bấm nút [🎙 GHI ÂM] thoải mái!)*

### Bước 3: Trải nghiệm Hệ thống
1. Mở trình duyệt web và truy cập: **`http://localhost:5000`**
2. **Thử nghiệm Ghi âm (Acoustic):** Ở trang chủ, cuộn xuống phần Tiếng Bíp hoặc Tiếng Quạt. Chọn tab **GHI ÂM (MIC)** và nhấn nút. Hệ thống sẽ thu âm 3 giây từ máy bạn và chẩn đoán!
3. **Thử nghiệm Hardware Scan:** Bấm vào chữ **🖥 HARDWARE SCAN** trên thanh menu. Nếu chữ `AGENT ONLINE` hiện màu xanh, hệ thống đang lấy số liệu thật từ máy bạn.

---

## ⚙️ Trạm Quản Trị & Bảo Mật (Admin & Security)

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
