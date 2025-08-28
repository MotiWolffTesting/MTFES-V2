#!/bin/bash

# Retriever Service CLI Commands

# Build Docker image:
"docker build -t your-dockerhub-username/mtfes-retriever:latest -f retriever/Dockerfile ."

# Run locally with default settings:
"docker run -d --name retriever-local --network host \\"
"  -e MONGODB_ATLAS_URI=\"mongodb+srv://IRGC_NEW:iran135@cluster0.6ycjkak.mongodb.net/\" \\"
"  -e MONGODB_DB_NAME=\"IranMalDB\" \\"
"  -e MONGODB_COLLECTION_NAME=\"tweets\" \\"
"  -e KAFKA_BOOTSTRAP_SERVERS=\"localhost:9092\" \\"
"  -e TOPIC_RAW_ANTISEMITIC=\"raw_tweets_antisemitic\" \\"
"  -e TOPIC_RAW_NOT_ANTISEMITIC=\"raw_tweets_not_antisemitic\" \\"
"  -e RETRIEVER_BATCH_SIZE=\"100\" \\"
"  -e RETRIEVER_INTERVAL_SECONDS=\"60\" \\"
"  -v /tmp/retriever_state.json:/tmp/retriever_state.json \\"
"  your-dockerhub-username/mtfes-retriever:latest"

# Push to Docker Hub:
"docker push your-dockerhub-username/mtfes-retriever:latest"

# Stop container:
"docker stop retriever-local && docker rm retriever-local"

# View logs:
"docker logs -f retriever-local"