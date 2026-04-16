# Sử dụng Python phiên bản slim cho nhẹ
FROM python:3.11-slim

# Cài đặt các thư viện hệ thống cần thiết cho mysql-connector
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file source code vào container
COPY . .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir flask mysql-connector-python

# Mở cổng 5000
EXPOSE 5000

# Lệnh chạy ứng dụng
CMD ["python", "app.py"]
