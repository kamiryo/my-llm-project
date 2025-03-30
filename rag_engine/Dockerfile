# rag_engine/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y unzip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]