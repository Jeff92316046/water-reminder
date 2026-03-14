FROM python:3.13-slim

# 從 GitHub 容器註冊表取得最新的 uv 執行檔
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 複製專案依賴定義檔
COPY pyproject.toml uv.lock ./

# 使用 uv 同步依賴，這會自動建立 .venv 並安裝 packages
RUN uv sync --frozen

# 複製程式碼
COPY src/ ./src/

# 將虛擬環境的執行路徑加入環境變數
ENV PATH="/app/.venv/bin:$PATH"

# 啟動應用程式
CMD ["python", "src/water_reminder.py"]
