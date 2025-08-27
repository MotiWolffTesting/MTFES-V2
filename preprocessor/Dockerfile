FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFED=1

WORKDIR /app

RUN apt-get updae && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY preprocessor/requirements.txt /app/requirements.txt
RUN pip install --no_cache-dir -r /app/requirements.txt && \
    python - <<'PY'
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
PY

COPY preprocessor /app/preprocessor

ENV PREPROCESSOR_GROUP_ID=preprocessor-group \
    PREPROCESSOR_CONSUME_TOPICS=raw_tweets_antisemitic,raw_tweets_not_antisemitic \
    TOPIC_PREPROCESSED_ANTISEMITIC=preprocessed_tweets_antisemitic \
    TOPIC_PREPROCESSED_NOT_ANTISEMITIC=preprocessed_tweets_not_antisemitic \
    PREPROCESSOR_LANGUAGE=english

CMD ["python", "-m", "preprocessor.src.main"]

