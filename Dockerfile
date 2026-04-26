# Sử dụng Python phiên bản slim cho nhẹ
FROM python:3.11-slim

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file requirements (nếu có) hoặc copy toàn bộ code
COPY . .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir \
    flask \
    mysql-connector-python \
    requests \
    psutil \
    numpy \
    scipy \
    flask-cors

# Mở cổng 5000 (Web) và 5001 (Agent nếu chạy chung)
EXPOSE 5000
EXPOSE 5001

# Lệnh chạy mặc định (sẽ bị ghi đè trong docker-compose nếu cần)
CMD ["python", "app.py"]
