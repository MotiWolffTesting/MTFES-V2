# Malicious Text Feature Engineering System (Week_11_Kafka_Malicious_Text)

Week_11_Kafka_Malicious_Text-V2 is a modular system for processing, enriching, and persisting text data, designed for scalable deployment and feature engineering on malicious or antisemitic content. It uses Kafka for inter-service communication and MongoDB for storage.

## Collaborators
- Ahron Frenkel
- Moti Wolff

## Features
- Modular microservices for retrieval, preprocessing, enrichment, and persistence
- Kafka-based streaming pipeline
- MongoDB Atlas (or local MongoDB) integration
- Text processing: sentiment analysis, weapon detection, feature extraction
- Dockerized for local and cloud deployment

## Tech Stack
- Python 3.11
- Kafka, MongoDB
- FastAPI (for dataretrieval service)
- PyMongo, Pandas, NLTK (VADER)
- Docker, OpenShift (optional)

## Project Layout
```
MTFES-V2/
  docker-compose.yaml
  README.md
  configs/
    kafka_config.yaml
    mongo_config.yaml
  dataretrieval/
    Dockerfile
    requirements.txt
    src/
      app.py
      routes.py
  enricher/
    Dockerfile
    requirements.txt
    src/
      enricher.py
      kafka_handler.py
      sentiment.py
      weapons.py
      timetsamp_extractor.py
      main.py
  persister/
    Dockerfile
    requirements.txt
    src/
      main.py
      mongo_handler.py
      persister.py
  preprocessor/
    Dockerfile
    requirements.txt
    src/
      main.py
      kafka_handler.py
      preprocessor.py
  retriever/
    Dockerfile
    requirements.txt
    src/
      main.py
      kafka_producer.py
      retriever.py
      config.py
  scripts/
    local_kafka.sh
    local_mongo.sh
    retriever_cli.sh
    preprocessor_cli.sh
    enricher_cli.sh
    persister_cli.sh
    dataretrieval_cli.sh
    openshift_commands.sh
    docker_build_push.sh
```

## Configuration
Set environment variables for each service as needed. Example for retriever:
- `MONGODB_ATLAS_URI`: MongoDB connection string
- `MONGODB_DB_NAME`: Database name
- `MONGODB_COLLECTION_NAME`: Collection name
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka server address
- `TOPIC_RAW_ANTISEMITIC`, `TOPIC_RAW_NOT_ANTISEMITIC`: Kafka topics

## Local Development
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies for each service
pip install -r retriever/requirements.txt
pip install -r preprocessor/requirements.txt
pip install -r enricher/requirements.txt
pip install -r persister/requirements.txt
pip install -r dataretrieval/requirements.txt

# Start local Kafka and MongoDB (see scripts/)
./scripts/local_kafka.sh
./scripts/local_mongo.sh

# Run a service (example: retriever)
python retriever/src/main.py

# Test FastAPI endpoints (dataretrieval)
python -m uvicorn dataretrieval/src/app:app --host 0.0.0.0 --port 8000 --reload
curl http://127.0.0.1:8000/health
open http://127.0.0.1:8000/docs
```

## Docker & Deployment
Each service has its own Dockerfile. Use `docker-compose.yaml` for local orchestration.
```bash
# Build all services
docker-compose build
# Start all services
docker-compose up
```

## OpenShift (optional)
See `scripts/openshift_commands.sh` for deployment automation.

## Endpoints (dataretrieval)
- `GET /health` – service liveness
- `GET /data` – processed records as JSON
- `GET /refresh` – re-fetch and re-process
- `GET /docs` – interactive API docs

## Troubleshooting
- Ensure all environment variables are set for each service
- Check Kafka and MongoDB are running and accessible
- Use the CLI scripts in `scripts/` for local testing

## License
MIT
 