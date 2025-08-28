#!/bin/bash

# Enricher Service CLI Commands

# Build Docker image:
"docker build -t your-dockerhub-username/mtfes-enricher:latest -f enricher/Dockerfile ."

# Run locally with default settings (host network):
"docker run -d --name enricher-local --network host \
  -e KAFKA_BOOTSTRAP_SERVERS=\"localhost:9092\" \
  -e ENRICHER_GROUP_ID=\"enricher_group\" \
  -e ENRICHER_CONSUME_TOPIC_ANTISEMITIC=\"preprocessed_tweets_antisemitic\" \
  -e ENRICHER_CONSUME_TOPIC_NOT_ANTISEMITIC=\"preprocessed_tweets_not_antisemitic\" \
  -e ENRICHER_PRODUCE_TOPIC_ANTISEMITIC=\"enriched_preprocessed_tweets_antisemitic\" \
  -e ENRICHER_PRODUCE_TOPIC_NOT_ANTISEMITIC=\"enriched_preprocessed_tweets_not_antisemitic\" \
  your-dockerhub-username/mtfes-enricher:latest"

# Push to Docker Hub:
"docker push your-dockerhub-username/mtfes-enricher:latest"

# Stop container:
"docker stop enricher-local && docker rm enricher-local"

# View logs:
"docker logs -f enricher-local"