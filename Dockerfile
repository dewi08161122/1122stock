# 1. 使用 Python 官方輕量版作為基底
FROM python:3.9-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 先複製環境清單並安裝，這樣可以利用快取加速之後的打包
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製所有程式碼到容器中
COPY . .

# 5. 告訴 Docker 程式會跑在 8000 Port
EXPOSE 8000

# 6. 啟動指令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]