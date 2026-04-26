@echo off
title EXPERT-SYS HARDWARE AGENT
color 0b

echo =======================================================
echo   KHOI DONG CAM BIEN PHAN CUNG (HARDWARE AGENT)
echo =======================================================
echo.
echo [*] Dang kiem tra thu vien Python...
pip install flask flask-cors psutil sounddevice numpy scipy wmi --quiet

echo [*] HUONG DAN CHO BAN CUA TAN:
echo     ---------------------------------------------------
echo     1. Luon giu cua so nay mo khi dang dung Web.
echo     2. Neu muon lay nhiet do CPU THUAN TUY (Real Data):
echo        - Hay mo phan mem LibreHardwareMonitor.exe
echo        - Chuot phai chon "Run as Administrator".
echo     3. Neu khong mo, he thong se tu dong GIA LAP nhiet do 
echo        dua tren tai CPU thuc (Smart Simulation).
echo     ---------------------------------------------------
echo.
echo [*] Dang bat Agent tai cong 5001...
python hardware_agent.py

pause
