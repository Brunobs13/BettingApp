FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY web ./web
COPY configs ./configs

ENV PYTHONPATH=/app/src
ENV BETTING_LOG_PATH=artifacts/events.jsonl
ENV LOG_LEVEL=INFO

EXPOSE 8080
CMD ["uvicorn", "betting_app.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
