#!/bin/bash

# Build all images:
"docker build -t your-dockerhub-username/mtfes-retriever:latest -f retriever/Dockerfile ."
"docker build -t your-dockerhub-username/mtfes-preprocessor:latest -f preprocessor/Dockerfile ."
"docker build -t your-dockerhub-username/mtfes-enricher:latest -f enricher/Dockerfile ."
"docker build -t your-dockerhub-username/mtfes-persister:latest -f persister/Dockerfile ."
"docker build -t your-dockerhub-username/mtfes-dataretrieval:latest -f dataretrieval/Dockerfile ."

# Push all images:
"docker push your-dockerhub-username/mtfes-retriever:latest"
"docker push your-dockerhub-username/mtfes-preprocessor:latest"
"docker push your-dockerhub-username/mtfes-enricher:latest"
"docker push your-dockerhub-username/mtfes-persister:latest"
"docker push your-dockerhub-username/mtfes-dataretrieval:latest"