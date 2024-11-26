# Sử dụng image Python 3.10
FROM python:3.10-slim

# Cài đặt Tesseract OCR và ngôn ngữ Tiếng Việt
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-vie \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép các file requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn
COPY . .

# Chạy bot
CMD ["python", "botbo.py"]