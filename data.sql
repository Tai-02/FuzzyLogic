CREATE DATABASE IF NOT EXISTS expert_system;

USE expert_system;

-- =============================================
-- Bảng: admins (Tài khoản quản trị)
-- Password được hash bằng werkzeug.security
-- Tài khoản mặc định: admin / admin123
-- =============================================
DROP TABLE IF EXISTS admins;
 
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
 
-- Tài khoản mặc định: admin / admin123
INSERT INTO admins (username, password_hash) VALUES (
    'admin',
    'scrypt:32768:8:1$kjWX2eCGiBuhADGW$a5cac878fa193b70a7077e4b8b99a2bc38136da37336359a84f784cfd614931ee04536c629323ce4c3579423d01879fa8613589c7a2cac7086b44fdd83d1e7d3'
);


-- =============================================
-- Bảng: rules (Cơ sở luật chẩn đoán)
-- =============================================
DROP TABLE IF EXISTS rules;

CREATE TABLE rules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conditions TEXT NOT NULL,
    conclusion TEXT NOT NULL,
    solution TEXT NOT NULL
);

-- =============================================
-- Nguồn: Bassil (2012)
-- Table 1 (trang 15) — Original 30 Diagnostic Rules
-- =============================================

-- Nhóm: Audio (Âm thanh)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Audio, Không nhận diện được Sound Card', 'Sound Card bị hỏng hoặc chưa được cài đặt', 'Thay thế Sound Card'),
('Audio, Cảnh báo lỗi Driver', 'Xung đột Driver hoặc Driver không tương thích', 'Cài đặt Driver phù hợp'),
('Audio, Âm thanh bị nhiễu sóng', 'Nhiễu tín hiệu (Signal Interference)', 'Tránh xa các nguồn phát sóng Radio (RF)'),
('Audio, Loa hoặc Microphone không hoạt động', 'Cắm sai cổng (Jacks)', 'Cắm lại đúng cổng');

-- =============================================
-- Nhóm: BIOS
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('BIOS, Lỗi sai ngày tháng hoặc năm nhuận', 'Phiên bản BIOS đã cũ', 'Cập nhật Flash BIOS'),
('BIOS, Không thể cập nhật Flash BIOS', 'BIOS đang bị khóa ghi (Write-Protected)', 'Tắt chế độ khóa ghi'),
('BIOS, Không thể truy cập vào BIOS', 'BIOS đang bị khóa mật khẩu', 'Xóa mật khẩu BIOS (Clear CMOS)');

-- =============================================
-- Nhóm: Hard Disk (Ổ cứng)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Hard Disk, Không nhận đủ dung lượng ổ cứng', 'Phiên bản BIOS đã cũ', 'Cập nhật BIOS'),
('Hard Disk, Ổ cứng UDMA không chạy hết tốc độ', 'BIOS cũ hoặc cáp IDE không tương thích', 'Cập nhật BIOS hoặc thay cáp IDE'),
('Hard Disk, Lỗi ổ IDE chưa sẵn sàng khi khởi động', 'Ổ cứng khởi động vòng quay quá chậm', 'Bật hoặc tăng độ trễ (Predelay-time) trong BIOS'),
('Hard Disk, Lỗi phân vùng ổ cứng không hợp lệ', 'Ổ cứng chưa được phân vùng', 'Dùng FDISK/Diskpart để tạo phân vùng hợp lệ'),
('Hard Disk, Lỗi định dạng ổ cứng', 'Ổ cứng chưa được Format', 'Format lại ổ cứng'),
('Hard Disk, Hiện cảnh báo SMART', 'Phát hiện lỗi cơ học nghiêm trọng', 'Sao lưu dữ liệu ngay lập tức và thay ổ cứng mới');

-- =============================================
-- Nhóm: Keyboard (Bàn phím)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Keyboard, Phím Num Lock tắt khi khởi động máy', 'Num Lock bị tắt mặc định trong BIOS', 'Bật Num Lock trong BIOS'),
('Keyboard, Bàn phím chập chờn', 'Cáp bàn phím hoặc cổng cắm bị lỗi', 'Kiểm tra cáp hoặc cổng cắm bằng đồng hồ VOM'),
('Keyboard, Phím bị kẹt cứng', 'Bàn phím bị đổ nước hoặc kẹt rác', 'Tháo nút phím và vệ sinh sạch sẽ');

-- =============================================
-- Nhóm: Mouse (Chuột)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Mouse, Không nhận diện được Chuột', 'Xung đột tài nguyên phần cứng', 'Dùng Windows Device Manager để tìm và sửa lỗi xung đột'),
('Mouse, Không dùng được cổng PS/2', 'Cổng PS/2 bị vô hiệu hóa', 'Bật cổng PS/2 trong BIOS'),
('Mouse, Con trỏ chuột bị giật lag', 'Cảm biến chuột bị dơ', 'Vệ sinh cảm biến chuột'),
('Mouse, Chuột chạy trong Windows nhưng không chạy trong DOS', 'Chưa nạp DOS Driver', 'Cài đặt DOS Mouse Driver');

-- =============================================
-- Nhóm: Power Supply (Nguồn điện - PSU)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Power Supply, Hệ thống tự khởi động lại (Reboots)', 'Điện áp (Voltage) không ổn định vượt ngưỡng', 'Kiểm tra Nguồn (PSU), thay thế nếu bị lỗi'),
('Power Supply, Lỗi sập nguồn sau khi gắn thêm linh kiện', 'Linh kiện mới tiêu thụ quá nhiều điện năng 5V', 'Thay Nguồn (PSU) có công suất 300W trở lên'),
('Power Supply, Ổ cứng hoặc Quạt không quay', 'Nguồn bị lỗi hoặc quá tải', 'Thay Nguồn (PSU) có công suất cao hơn'),
('Power Supply, Không sáng đèn, không quay quạt', 'Nguồn bị chết hoàn toàn', 'Thay Nguồn (PSU) mới');

-- =============================================
-- Nhóm: Processor (Vi xử lý - CPU)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Processor, Máy không chạy sau khi thay CPU', 'Lắp đặt CPU chưa đúng cách', 'Tháo ra và lắp lại CPU cùng tản nhiệt (Heatsink)'),
('Processor, Nhận diện sai CPU khi POST', 'Phiên bản BIOS đã cũ', 'Cập nhật BIOS');

-- =============================================
-- Nhóm: Serial ATA
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Serial ATA, Không nhận diện được ổ cứng SATA', 'Cổng SATA đang bị vô hiệu hóa', 'Bật cổng SATA trên Mainboard'),
('Serial ATA, Không dùng được cổng Serial onboard', 'Cổng Serial bị vô hiệu hóa trong BIOS', 'Bật cổng Serial'),
('Serial ATA, Xung đột cổng Serial với thiết bị khác', 'Lỗi xung đột IRQ hoặc địa chỉ I/O', 'Chỉnh lại IRQ hoặc tắt cổng Serial');

-- =============================================
-- Nhóm: Startup (Khởi động)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Startup, Máy lên nguồn nhưng không xuất hình', 'Lỗi Video Card (Card màn hình rời)', 'Thay thế hoặc sửa chữa Video Card'),
('Startup, Hệ thống kêu bíp nhiều lần', 'Lỗi phần cứng nghiêm trọng (Fatal Hardware Errors)', 'Kiểm tra các linh kiện đang bị lỗi (RAM, VGA)'),
('Startup, Hệ thống không tìm thấy ổ cứng boot', 'Lỗi thứ tự khởi động (Boot Priority)', 'Vào BIOS cài đặt ổ cứng làm thiết bị khởi động đầu tiên'),
('Startup, Máy không chạy sau khi gắn thêm Card rời', 'Xung đột phần cứng hoặc Card bị lỗi', 'Tháo tất cả các Card mới gắn và thử lại');

-- =============================================
-- Nguồn: Mandal, Chatterjee & Neogi (2013)
-- Bảng: Table 1 (trang 721) — Sound System Problem
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Audio, Loa không phát ra tiếng',
 'Âm lượng bị tắt (Muted) hoặc mức 0',
 'Nhấp đúp vào biểu tượng loa trên thanh taskbar. Kiểm tra tùy chọn Mute và điều chỉnh âm lượng.'),

('Audio, Âm lượng quá nhỏ',
 'Mức âm lượng hệ thống cài đặt quá thấp',
 'Nhấn nút tăng âm lượng trên bàn phím hoặc điều chỉnh thanh trượt âm lượng trên Windows.'),

('Audio, Hoàn toàn không có tín hiệu âm thanh',
 'Chưa cắm cáp âm thanh (Speaker Cables)',
 'Tham khảo sách hướng dẫn để cắm cáp loa đúng vào cổng Audio Out (màu xanh lá).'),

('Audio, Âm thanh bị méo tiếng',
 'Mức âm lượng cài đặt quá cao (Quá công suất)',
 'Giảm mức âm lượng hệ thống hoặc loa ngoài xuống mức vừa phải.'),

('Audio, Không có âm thanh trong Windows',
 'Lỗi trong cài đặt Volume Control',
 'Mở Volume Mixer trên Windows và đảm bảo các ứng dụng không bị kéo thanh trượt xuống đáy.'),

('Audio, Windows không nhận diện được thiết bị âm thanh',
 'Audio Driver chưa cài đặt hoặc bị hỏng',
 'Vào Device Manager, xóa Audio Driver cũ và khởi động lại máy để tự cài đặt lại.');

-- =============================================
-- Nguồn: Abu-Naser & Al-Dahdooh (2019)
-- Trang 3-4 — VGA & Power Supply rules
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Startup, Màn hình không hiển thị gì',
 'Lỗi cáp nguồn, cáp màn hình, hoặc hỏng VGA Card',
 'Cắm lại cáp nguồn, cáp màn hình. Nếu không được hãy thay thế VGA Card.'),

('Startup, Màn hình bị nhòe hoặc sai màu',
 'VGA Card cắm lỏng hoặc lỗi VRAM',
 'Tắt máy, tháo VGA Card ra vệ sinh chân cắm (PCIe) và cắm chặt lại.'),

('Startup, Hệ thống tự động Restart ngẫu nhiên',
 'Điện áp Nguồn (PSU) không ổn định',
 'Test Nguồn bằng đồng hồ DMM. Thay Nguồn công suất thực cao hơn (ví dụ 400W+) nếu thông số bị tụt áp.');

-- =============================================
-- Chain Rules — thiết kế bởi Nhóm 8
-- =============================================

-- Chuỗi 1: BIOS cũ → không nhận HDD → không boot được
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Hard Disk, Không nhận đủ dung lượng ổ cứng',
 'Phiên bản BIOS đã cũ',
 'Cập nhật BIOS lên phiên bản mới nhất từ trang chủ nhà sản xuất.'),

('Startup, Phiên bản BIOS đã cũ',
 'Hệ thống có thể không nhận diện được phần cứng đời mới',
 'Cập nhật BIOS ngay lập tức. BIOS cũ thường gây lỗi không tương thích với ổ cứng và CPU mới.');

-- Chuỗi 2: PSU lỗi → HDD không quay → không tìm thấy ổ cứng
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Power Supply, Ổ cứng hoặc Quạt không quay',
 'Nguồn bị lỗi hoặc quá tải',
 'Thay Nguồn (PSU) có công suất 300W trở lên.'),

('Startup, Nguồn bị lỗi hoặc quá tải',
 'Các ổ đĩa lưu trữ (Storage Devices) không nhận đủ điện',
 'Sau khi thay Nguồn, hãy kiểm tra lại các đầu cắm nguồn SATA xem đã cắm chặt vào ổ cứng chưa.');

-- Chuỗi 3: RAM lỗi → không POST → hệ thống beep
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Startup, Hệ thống kêu bíp nhiều lần',
 'Phát hiện lỗi phần cứng nghiêm trọng',
 'Kiểm tra các linh kiện đang bị lỗi — tháo ra cắm lại RAM, VGA Card và các Card mở rộng.'),

('Startup, Phát hiện lỗi phần cứng nghiêm trọng',
 'Quá trình POST thất bại — Hệ thống bị treo',
 'Boot máy với cấu hình tối giản: CPU + 1 thanh RAM + dùng iGPU. Gắn thêm từng linh kiện để tìm ra món nào bị hỏng.');


-- ==============================================================
-- [MODULE] CHẨN ĐOÁN NHIỆT ĐỘ (FUZZY TEMPERATURE MODULE)
-- ==============================================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Cooling, Quạt kêu to (Loud fan noise)', 'Quạt tản nhiệt hoạt động tối đa', 'Kiểm tra xem hệ thống có đang quá tải nhiệt không.'),
('Cooling, Máy tự tắt đột ngột (Random Shutdown)', 'Hệ thống tự tắt đột ngột', 'Dấu hiệu của việc sụt nguồn hoặc quá nhiệt nghiêm trọng.'),
('Performance, Máy chạy chậm dần (Lagging)', 'Hệ thống phản hồi chậm', 'Kiểm tra tài nguyên CPU/RAM hoặc hệ thống tản nhiệt.');

INSERT INTO rules (conditions, conclusion, solution) VALUES
('Temp_Danger', 'Hệ thống đang quá nhiệt ở mức Đe dọa phần cứng', 'Lập tức lưu dữ liệu và tắt máy. Kiểm tra lại toàn bộ hệ thống tản nhiệt ngay khi máy nguội.'),
('Temp_Warning', 'Hệ thống đang hoạt động ở mức nhiệt độ Cảnh báo', 'Theo dõi sát sao. Nếu không chạy tác vụ nặng (Game/Render) mà vẫn đạt mức này, hãy lên lịch vệ sinh máy.');

INSERT INTO rules (conditions, conclusion, solution) VALUES
('Temp_Danger, Quạt kêu to (Loud fan noise)', 
 'Quá nhiệt nghiêm trọng dẫn đến hạ xung (Thermal Throttling)', 
 'Vệ sinh toàn bộ hệ thống tản nhiệt, tra lại keo tản nhiệt chất lượng cao.'),

('Temp_Danger, Máy tự tắt đột ngột (Random Shutdown)', 
 'Bo mạch chủ kích hoạt ngắt điện tự vệ do chạm ngưỡng Tjunction Max', 
 'Tuyệt đối không bật lại máy. Kiểm tra ngay tình trạng bơm tản nhiệt hoặc quạt CPU.'),

('Temp_Warning, Máy chạy chậm dần (Lagging)', 
 'Hệ thống tản nhiệt bắt đầu kém hiệu quả, không duy trì được xung nhịp tối đa', 
 'Kê cao đáy máy để tăng luồng khí (Airflow), kiểm tra môi trường phòng.');

-- ==============================================================
-- [MODULE] LUẬT LIÊN HỢP ĐA BIẾN (BEEP + NHIỆT ĐỘ + TRIỆU CHỨNG)
-- ==============================================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('continuous, Temp_Danger', 
 'Bo mạch chủ chạm nguồn do quá tải nhiệt / Cảnh báo nhiệt khẩn cấp từ BIOS', 
 'Ngắt điện khẩn cấp ngay lập tức. Không cố bật lại máy. Chờ máy nguội hẳn, tháo nắp hông và kiểm tra xem có tụ điện nào bị phù nứt, hoặc quạt CPU có bị kẹt cứng không.'),

('very long, Quạt kêu to (Loud fan noise)', 
 'Nguồn điện (PSU) hoạt động quá mức hoặc sắp hỏng do quá nhiệt', 
 'Tiếng bíp rất dài kèm tiếng quạt hú to cho thấy Nguồn máy tính (Power Supply) đang gặp trục trặc dòng điện. Tắt máy và thay thế Nguồn công suất thực cao hơn.'),

('8 beeps, Startup, Máy lên nguồn nhưng không xuất hình', 
 'VGA Card (Card màn hình rời) bị lỗi Video RAM', 
 '8 tiếng bíp là mã lỗi đặc trưng của VRAM. Kết hợp với việc máy lên nguồn nhưng không xuất hình, 100% card màn hình của bạn đã hỏng. Cần thay thế card mới hoặc tháo card rời để cắm thẳng dây màn hình vào Mainboard (dùng iGPU).');