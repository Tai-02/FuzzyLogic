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
-- (hash bằng werkzeug generate_password_hash)
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
-- Nhóm: Audio (Âm thanh)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Audio, Sound Card can\'t be Detected', 'Damaged or Sound Card Not Installed', 'Replace Sound Card'),
('Audio, Driver Warning', 'Driver Conflict or Incompatible Driver', 'Install The Appropriate Driver'),
('Audio, Scratchy Sound', 'Signal Interference', 'Stay Away from Radio Frequency Sources'),
('Audio, Speaker or Microphone won\'t Work', 'Incorrect Jacks', 'Use Proper Jacks');

-- =============================================
-- Nhóm: BIOS
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('BIOS, Calendar-Related and Leap-Year Bugs', 'BIOS is out-of-date', 'Upgrade Flash BIOS'),
('BIOS, Can\'t Install Flash BIOS Update', 'BIOS is Write-Protected', 'Disable Write-Protection'),
('BIOS, Can\'t Access BIOS', 'BIOS is Password Protected', 'Remove Password');

-- =============================================
-- Nhóm: Hard Disk (Ổ cứng)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Hard Disk, Can\'t Access Full Capacity over 8.4GB', 'BIOS is Out-of-Date', 'Upgrade BIOS'),
('Hard Disk, Can\'t Use UDMA Drives at Full Speed', 'BIOS is Out-of-Date or Incompatible IDE Cable', 'Upgrade BIOS or Replace IDE Cable'),
('Hard Disk, IDE Drive not Ready Errors During Startup', 'Drive not Spinning Up Fast Enough at Startup', 'Enable or Increase Hard Disk Predelay-time'),
('Hard Disk, Invalid Drive Specification Error', 'Drive has not Been Partitioned', 'Run FDISK to Create Valid Partitions'),
('Hard Disk, Invalid Media Type Error', 'Drive not Yet Formatted', 'Format your Drive'),
('Hard Disk, SMART Warning Displayed', 'Serious Mechanical Problems are Detected', 'Backup & Replace Your Drive');

-- =============================================
-- Nhóm: Keyboard (Bàn phím)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Keyboard, Num Lock Stays Off when Starting System', 'Num Lock Shut off in BIOS', 'Turn on Num Lock in BIOS'),
('Keyboard, Intermittent Keyboard Failures', 'Keyboard Cable or Keyboard Jack Might be Defective', 'Test Keyboard Cable or Jack with Digital Multimeter'),
('Keyboard, Keys are Sticking', 'Keyboard might have Spilled Drink or Trapped Debris', 'Remove Keytops and Clean under Keys, or Wash-out Keyboard');

-- =============================================
-- Nhóm: Mouse (Chuột)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Mouse, Mouse can\'t be Detected', 'Hardware Resource Conflict', 'Use Windows Device Manager to Find Conflicts and Resolve them'),
('Mouse, Can\'t use PS/2 Mouse', 'PS/2 Mouse Port Might be Disabled', 'Enable PS/2 Mouse Port'),
('Mouse, Mouse Pointer Jerks Onscreen', 'Mouse Ball or Rollers are Dirty', 'Clean Mouse Mechanism'),
('Mouse, Mouse Works in Windows but Not in DOS', 'DOS Driver Must be Loaded from AUTOEXEC.BAT or CONFIG.SYS', 'Install DOS Mouse Driver, and Reference it in Startup Files');

-- =============================================
-- Nhóm: Power Supply (Nguồn điện)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Power Supply, System Reboots', 'Power Good Voltage Level out of Limits', 'Check Power Supply with DMM; Replace Power Supply if Defective'),
('Power Supply, Fails after Additional Components Added', 'New Components Require more 5V Power than Old Power Supply can Provide', 'Replace Failed Unit with a 300-watt or Larger Unit'),
('Power Supply, Hard Disk or Fan won\'t Turn', 'Defective or Overloaded Power Supply', 'Replace Failed Unit with a 300-watt or Larger Unit'),
('Power Supply, No Leds No Fans are Turn', 'Defective Power Supply', 'Replace Power Supply');

-- =============================================
-- Nhóm: Processor (Vi xử lý)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Processor, System won\'t Start After New Processor Installed', 'Processor not Properly Installed', 'Reseat and Reinstall Processor and Heatsink'),
('Processor, Improper CPU Identification during POST', 'Old BIOS', 'Upgrade BIOS');

-- =============================================
-- Nhóm: Serial ATA
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Serial ATA, Drives are not Recognized by System', 'Some Systems have Disabled Serial ATA Ports', 'Enable Onboard Serial ATA ports'),
('Serial ATA, Can\'t use Onboard Serial Port', 'Port Might be Disabled in BIOS', 'Enable Port'),
('Serial ATA, Conflict between Onboard Serial Port and other Device', 'IRQ or I/O port Address Conflicts with other Device', 'Adjust IRQ or I/O port Address in Use, or Disable Port');

-- =============================================
-- Nhóm: Startup (Khởi động)
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Startup, No Live Screen But System is On', 'Video Card Problem', 'Replace your Video Card'),
('Startup, System Beeps Several Times', 'Fatal Hardware Errors', 'Check for Any Defective Hardware'),
('Startup, System Can\'t Find any Hard Drive', 'Boot Priority Errors', 'Set Hard Drive as the 1st Booting Device'),
('Startup, Computer won\'t Start After Installing Card', 'Conflict or Defective Hardware', 'Remove all Connected Cards and Try Again');

-- =============================================
-- LUẬT CHUỖI (CHAIN RULES)
-- Sử dụng kết luận của các luật trước làm điều kiện
-- để Forward Chaining chạy nhiều vòng (multi-pass)
-- =============================================

-- Chain 1: Lỗi nguồn điện nghiêm trọng
-- Nếu vừa phát hiện PSU voltage lỗi + PSU quá tải → Critical PSU Failure
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Power Good Voltage Level out of Limits, Defective or Overloaded Power Supply',
 'Critical PSU Failure — Immediate Replacement Required',
 'Multiple PSU failure indicators detected simultaneously.\n1) Disconnect all power cables immediately.\n2) Test PSU with multimeter — check +3.3V, +5V, +12V rails.\n3) Replace PSU with unit rated 300W or higher.\n4) After replacing, run burn-in test for 24 hours to verify stability.');

-- Chain 2: Lỗi hiển thị + phần cứng nghiêm trọng → mainboard
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Video Card Problem, Fatal Hardware Errors',
 'Mainboard-Level Display Subsystem Failure',
 'Both video and fatal hardware errors indicate mainboard-level failure.\n1) Remove all expansion cards.\n2) Test with integrated graphics if available.\n3) Try a known-good video card in another PCIe slot.\n4) If all fail, the PCIe slot or mainboard chipset is likely damaged — consider mainboard replacement.');

-- Chain 3: BIOS lỗi thời + Ổ cứng không khởi tạo được
INSERT INTO rules (conditions, conclusion, solution) VALUES
('BIOS is Out-of-Date, Drive has not Been Partitioned',
 'Storage Subsystem Initialization Failure',
 'Both BIOS and drive partition issues detected.\n1) Update BIOS firmware first.\n2) After BIOS update, run FDISK to create partitions.\n3) Format the drive.\n4) If drive still not recognized, check SATA cable and port.');

-- Chain 4: BIOS lỗi + mật khẩu khóa → Deadlock
INSERT INTO rules (conditions, conclusion, solution) VALUES
('BIOS is out-of-date, BIOS is Password Protected',
 'BIOS Access and Update Deadlock',
 'Cannot update BIOS because it is password-protected.\n1) Clear CMOS by removing battery for 30 seconds.\n2) Use motherboard jumper to reset BIOS password.\n3) After reset, immediately update BIOS firmware.\n4) Set a new documented password after update.');

-- Chain 5: PSU hỏng + Card xung đột → Toàn hệ thống
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Defective Power Supply, Conflict or Defective Hardware',
 'System-Wide Power and Hardware Conflict',
 'Power supply failure combined with hardware conflict indicates cascading system failure.\n1) Replace PSU first.\n2) Remove all non-essential cards and peripherals.\n3) Boot with minimal configuration (CPU + 1 RAM stick + onboard video).\n4) Add components one by one to isolate the conflict.');