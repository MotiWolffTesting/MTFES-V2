#!/bin/bash

# Persister Service CLI Commands

# Build Docker image:
"docker build -t your-dockerhub-username/mtfes-persister:latest -f persister/Dockerfile ."

# Run locally on bridge network, connecting to mtfes-mongo container:
"docker run -d --name persister-local \
  -e KAFKA_BOOTSTRAP_SERVERS=\"localhost:9092\" \
  -e PERSISTER_GROUP_ID=\"persister_group\" \
  -e TOPIC_ANTISEMITIC=\"enriched_preprocessed_tweets_antisemitic\" \
  -e TOPIC_NOT_ANTISEMITIC=\"enriched_preprocessed_tweets_not_antisemitic\" \
  -e MONGODB_URI=\"mongodb://mtfes-mongo:27017\" \
  -e MONGODB_DB_NAME=\"IranMalDBLocal\" \
  -e MONGODB_COLLECTION_ANTISEMITIC_NAME=\"tweets_antisemitic\" \
  -e MONGODB_COLLECTION_NOT_ANTISEMITIC_NAME=\"tweets_not_antisemitic\" \
  your-dockerhub-username/mtfes-persister:latest"

# Alternative: Run with host network, connecting to localhost Mongo (if you started Mongo with --network host)
"docker run -d --name persister-local --network host \
  -e KAFKA_BOOTSTRAP_SERVERS=\"localhost:9092\" \
  -e PERSISTER_GROUP_ID=\"persister_group\" \
  -e TOPIC_ANTISEMITIC=\"enriched_preprocessed_tweets_antisemitic\" \
  -e TOPIC_NOT_ANTISEMITIC=\"enriched_preprocessed_tweets_not_antisemitic\" \
  -e MONGODB_URI=\"mongodb://localhost:27017\" \
  -e MONGODB_DB_NAME=\"IranMalDBLocal\" \
  -e MONGODB_COLLECTION_ANTISEMITIC_NAME=\"tweets_antisemitic\" \
  -e MONGODB_COLLECTION_NOT_ANTISEMITIC_NAME=\"tweets_not_antisemitic\" \
  your-dockerhub-username/mtfes-persister:latest"

# Push to Docker Hub:
"docker push your-dockerhub-username/mtfes-persister:latest"

# Stop container:
"docker stop persister-local && docker rm persister-local"

# View logs:
"docker logs -f persister-local"
