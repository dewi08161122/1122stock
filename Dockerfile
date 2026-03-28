# 1. 使用官方輕量版 Python 作為基底
FROM python:3.11-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 先複製依賴清單，利用 Docker 快取機制加速後續建構
COPY requirements.txt .

# 4. 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製專案所有程式碼到容器中
COPY . .

# 6. 暴露 FastAPI 預設的 8000 埠
EXPOSE 8000

# 7. 啟動指令 (使用 uvicorn)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]