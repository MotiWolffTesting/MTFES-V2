FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps (if needed for ssl, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY retriever/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY retriever /app/retriever

ENV MONGODB_DB_NAME=IranMalDB \
    MONGODB_COLLECTION_NAME=tweets \
    TOPIC_RAW_ANTISEMITIC=raw_tweets_antisemitic \
    TOPIC_RAW_NOT_ANTISEMITIC=raw_tweets_not_antisemitic \
    RETRIEVER_BATCH_SIZE=100 \
    RETRIEVER_INTERVAL_SECONDS=60

CMD ["python", "-m", "retriever.src.main"]
