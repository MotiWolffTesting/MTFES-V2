FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY dataretrieval/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY dataretrieval /app/dataretrieval

ENV LOCAL_MONGO_URI=mongodb://mongo:27017/ \
    LOCAL_MONGO_DB=IranMalDBLocal

EXPOSE 8080

CMD ["uvicorn", "dataretrieval.src.app:create_app", "--host", "0.0.0.0", "--port", "8080", "--factory"]


