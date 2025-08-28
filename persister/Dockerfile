FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY persister /app/persister

ENV MONGODB_DB_NAME=PersisterIranMalDB \
    MONGODB_COLLECTION_ANTISEMITIC_NAME=tweets_antisemitic \
    MONGODB_COLLECTION_NOT_ANTISEMITIC_NAME=tweets_not_antisemitic \
    PERSISTER_GROUP_ID=persister_group \
    TOPIC_ANTISEMITIC=enriched_preprocessed_tweets_antisemitic \
    TOPIC_NOT_ANTISEMITIC=enriched_preprocessed_tweets_not_antisemitic

CMD ["python", "-m", "persister.src.main"]