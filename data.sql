CREATE DATABASE IF NOT EXISTS expert_system;

USE expert_system;

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