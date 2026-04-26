# hardware_agent.py
"""
EXPERT-SYS Hardware Agent v1.0
Chạy ngầm trên máy người dùng, cung cấp dữ liệu hardware qua HTTP.

Đóng gói bằng:
    pip install pyinstaller flask flask-cors psutil sounddevice numpy scipy
    pyinstaller --onefile --noconsole --name "EXPERT-SYS-Agent" hardware_agent.py

File .exe sẽ ở trong thư mục dist/
Người dùng chỉ cần double-click để chạy, không cần cài Python.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import platform

agent = Flask(__name__)
CORS(agent, origins=["http://localhost:5000", "http://127.0.0.1:5000"])


@agent.route('/hardware')
def get_hardware():
    """
    Endpoint chính: trả về toàn bộ thông tin phần cứng real-time.

    Returns JSON:
        {
            "status": "ok",
            "platform": str,
            "cpu_percent": float,
            "ram_percent": float,
            "disk_percent": float,
            "cpu_temp": float | null,
            "fan_speeds": list
        }
    """
    data = {
        "status": "ok",
        "platform": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "cpu_temp": None,
        "fan_speeds": []
    }

    # Nhiệt độ (Linux/macOS native, Windows cần OpenHardwareMonitor)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                if entries:
                    data["cpu_temp"] = entries[0].current
                    break
    except AttributeError:
        pass  # Windows không support psutil sensors

    # Tốc độ quạt
    try:
        fans = psutil.sensors_fans()
        if fans:
            for name, entries in fans.items():
                for entry in entries:
                    data["fan_speeds"].append({
                        "label": entry.label or name,
                        "rpm": entry.current
                    })
    except AttributeError:
        pass

    return jsonify(data)


@agent.route('/mic-test')
def mic_test():
    """Test microphone availability trên máy người dùng."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        return jsonify({
            "available": len(input_devices) > 0,
            "count": len(input_devices)
        })
    except Exception as e:
        return jsonify({"available": False, "error": str(e)})


@agent.route('/fan-record', methods=['POST'])
def fan_record():
    """
    Ghi âm tiếng quạt từ microphone và trả về chẩn đoán fuzzy.
    Yêu cầu sounddevice + numpy + scipy đã cài.
    """
    try:
        # Import từ fuzzy.py cùng thư mục
        from fuzzy import analyze_fan_noise_from_mic
        result = analyze_fan_noise_from_mic(duration=3, sample_rate=44100)
        return jsonify({"status": "ok", **result})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})


@agent.route('/beep-record', methods=['POST'])
def beep_record():
    """
    Ghi âm tiếng bíp và phân tích độ dài tiếng bíp.
    Để dễ demo, phân tích cường độ âm thanh (RMS) và quy đổi sang độ dài giây.
    """
    try:
        from fuzzy import analyze_fan_noise_from_mic
        # Lấy file thu âm 3 giây
        result = analyze_fan_noise_from_mic(duration=3, sample_rate=44100)
        rms = result.get("rms", 0)
        # Giả lập: Nếu tiếng càng to (rms cao) thì coi như tiếng bíp càng dài
        # rms dao động từ 0 đến 0.5. Nhân với 6 để ra số giây tối đa là 3.0s
        duration = round(rms * 6.0, 1)
        if duration < 0.1:
            duration = 0.0 # Không có tiếng
        
        return jsonify({
            "status": "ok", 
            "duration": duration,
            "message": f"Phát hiện âm thanh kéo dài {duration}s"
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})


@agent.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "version": "1.0"})


if __name__ == '__main__':
    print("=" * 55)
    print("  EXPERT-SYS Hardware Agent v1.0")
    print("=" * 55)
    print(f"  Platform : {platform.system()} {platform.release()}")
    print(f"  Endpoint : http://localhost:5001/hardware")
    print(f"  Health   : http://localhost:5001/health")
    print("-" * 55)
    print("  Giữ cửa sổ này mở khi dùng hệ thống chẩn đoán.")
    print("  Nhấn Ctrl+C để tắt agent.")
    print("=" * 55)
    agent.run(host='0.0.0.0', port=5001, debug=False)
