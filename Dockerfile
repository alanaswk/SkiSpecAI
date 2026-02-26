FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/tmp/hf \
    HF_HUB_CACHE=/tmp/hf/hub \
    TRANSFORMERS_CACHE=/tmp/hf/hub \
    PORT=8080

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY . .

RUN uv sync --frozen

EXPOSE 8080

CMD ["uv", "run", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8080"]