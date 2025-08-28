#!/bin/bash

# Preprocessor Service CLI Commands

# Build Docker image:
"docker build -t your-dockerhub-username/mtfes-preprocessor:latest -f preprocessor/Dockerfile ."

# Run locally with default settings:
"docker run -d --name preprocessor-local --network host \\"
"  -e KAFKA_BOOTSTRAP_SERVERS=\"localhost:9092\" \\"
"  -e PREPROCESSOR_GROUP_ID=\"preprocessor-group\" \\"
"  -e PREPROCESSOR_CONSUME_TOPICS=\"raw_tweets_antisemitic,raw_tweets_not_antisemitic\" \\"
"  -e TOPIC_PREPROCESSED_ANTISEMITIC=\"preprocessed_tweets_antisemitic\" \\"
"  -e TOPIC_PREPROCESSED_NOT_ANTISEMITIC=\"preprocessed_tweets_not_antisemitic\" \\"
"  -e PREPROCESSOR_LANGUAGE=\"english\" \\"
"  your-dockerhub-username/mtfes-preprocessor:latest"

# Push to Docker Hub:
"docker push your-dockerhub-username/mtfes-preprocessor:latest"

# Stop container:
"docker stop preprocessor-local && docker rm preprocessor-local"

# View logs:
"docker logs -f preprocessor-local"