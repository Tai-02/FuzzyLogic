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
-- Nguồn: Bassil (2012)
-- "A Simulation Model for an Expert PC Troubleshooter"
-- International Journal of Artificial Intelligence & Applications (IJAIA), Vol.3, No.2.
-- Table 1 (trang 15) — Original 30 Diagnostic Rules
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
-- Nguồn: Mandal, Chatterjee & Neogi (2013)
-- "Diagnosis and Troubleshooting of Computer Faults
--  Based on Expert System and Artificial Intelligence"
-- International Journal of Pure and Applied Mathematics,
-- Vol. 83, No. 5, pp. 717-729
-- Bảng: Table 1 (trang 721) — Sound System Problem
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Audio, No Sound From Speakers',
 'Volume Turned Off or Muted',
 'Double-click the speaker icon on the taskbar. Check that the Mute option is not selected and adjust volume.'),

('Audio, Volume Is Too Low',
 'Speaker Volume Set Too Low',
 'Press the Volume Up button on keyboard or double-click the speaker icon and drag the slider up.'),

('Audio, No Sound At All',
 'Speaker Cables Not Connected',
 'Refer to the quick setup guide for instructions on how to connect speakers to your computer.'),

('Audio, Sound Is Distorted',
 'Volume Level Set Too High',
 'Press Volume Down button on keyboard or double-click speaker icon and set volume to a lower level.'),

('Audio, No Sound In Windows',
 'Fault In Volume Control Settings',
 'Double-click the speaker icon on the Windows taskbar, click the slider and drag it up.'),

('Audio, Windows Does Not Detect Audio',
 'Audio Driver Not Installed or Corrupted',
 'Open Control Panel → Sound/Video/Game Controllers → Device Manager. Remove old audio driver and restart to reinstall.');

-- =============================================
-- Nguồn: Abu-Naser & Al-Dahdooh (2019)
-- "Design and Implementation of A Mobile Expert System
--  for Computer Hardware Troubleshooting"
-- ResearchGate, October 2019
-- Trang 3-4 — VGA & Power Supply rules
-- =============================================
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Startup, No Display On Monitor',
 'Failure In Power Cord, Monitor Cable, or VGA Card',
 'Reinstall power cable, fix or replace power supply, change monitor power cable or replace VGA card.'),

('Startup, Blurry or Distorted Display',
 'VGA Card Not Properly Installed',
 'Power off, reseat the VGA card firmly into the PCIe slot, secure the bracket screw, and restart.'),

('Startup, System Restarts Randomly',
 'Power Supply Voltage Unstable',
 'Test PSU with digital multimeter (DMM). Replace with a higher wattage unit (400W+) if readings are out of range.');

-- =============================================
-- Chain Rules — thiết kế bởi Nhóm 8
-- Kết luận của luật trước → điều kiện của luật sau
-- Mục đích: minh chứng Forward Chaining multi-pass
-- =============================================

-- Chuỗi 1: BIOS cũ → không nhận HDD → không boot được
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Hard Disk, Can\'t Access Full Capacity over 8.4GB',
 'BIOS is Out-of-Date',
 'Upgrade BIOS to latest version from manufacturer website.'),

-- Luật này dùng kết luận "BIOS is Out-of-Date" từ luật trên làm điều kiện
('Startup, BIOS is Out-of-Date',
 'System May Fail To Recognize New Hardware',
 'Update BIOS immediately. Old BIOS version causes incompatibility with modern drives and processors.');

-- Chuỗi 2: PSU lỗi → HDD không quay → không tìm thấy ổ cứng
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Power Supply, Hard Disk or Fan won\'t Turn',
 'Defective or Overloaded Power Supply',
 'Replace with 300W+ power supply unit.'),

('Startup, Defective or Overloaded Power Supply',
 'Storage Devices May Not Receive Sufficient Power',
 'After replacing PSU, check all SATA power connectors are firmly seated on drives.');

-- Chuỗi 3: RAM lỗi → không POST → hệ thống beep
INSERT INTO rules (conditions, conclusion, solution) VALUES
('Startup, System Beeps Several Times',
 'Fatal Hardware Errors Detected',
 'Check for any defective hardware — reseat RAM, GPU, and all expansion cards.'),

('Startup, Fatal Hardware Errors Detected',
 'POST Cannot Complete — System Halted',
 'Boot with minimal config: CPU + 1 RAM stick + no GPU (use iGPU). Add components one at a time to isolate the fault.');