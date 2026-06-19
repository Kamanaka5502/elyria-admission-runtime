FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ELYRIA_MODE=demo
ENV ELYRIA_DB_PATH=/app/data/elyria.db

WORKDIR /app

COPY requirements.txt pyproject.toml ./
COPY src ./src
COPY apps ./apps

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir -e . \
    && mkdir -p /app/data

EXPOSE 8080

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
