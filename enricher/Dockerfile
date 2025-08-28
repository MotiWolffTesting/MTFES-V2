FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/enricher

ENV ENRICHER_GROUP_ID=enricher_group \
    ENRICHER_CONSUME_TOPIC_ANTISEMITIC=preprocessed_tweets_antisemitic \
    ENRICHER_CONSUME_TOPIC_NOT_ANTISEMITIC=preprocessed_tweets_not_antisemitic \
    ENRICHER_PRODUCE_TOPIC_ANTISEMITIC=enriched_preprocessed_tweets_antisemitic \
    ENRICHER_PRODUCE_TOPIC_NOT_ANTISEMITIC=enriched_preprocessed_tweets_not_antisemitic

CMD ["python", "-m", "enricher.src.main"]