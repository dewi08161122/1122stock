# 1. 使用官方輕量版 Python 作為基底
FROM python:3.11-slim

WORKDIR /app

# 設定時區，確保爬蟲抓到的 date.today() 是台灣時間
ENV TZ=Asia/Taipei

# 安裝必要套件 (requests, mysql-connector-python, python-dotenv)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製爬蟲程式碼與共用的基礎建設 (infrastructure, models 等)
COPY . .

# 執行爬蟲主程式 (daily_crawler.py)
CMD ["python", "daily_crawler.py"]