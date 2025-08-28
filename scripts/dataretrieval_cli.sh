#!/bin/bash

# DataRetrieval Service CLI Commands

# Build Docker image:
"docker build -t your-username/mtfes-datarertieval:latest -f dataretrieval/Dockerfile ."

# Run locally with default settings
"docker run -d --name dataretrieval-local -p 8080:8080 \\"
"  -e LOCAL_MONGO_URI=\"mongodb://localhost:27017/\" \\"
echo "  -e LOCAL_MONGO_DB=\"IranMalDBLocal\" \\"
echo "  your-dockerhub-username/mtfes-dataretrieval:latest"

# Push to Docker Hub:
"docker push your-username/mtfes-dataretrieval:latest"

# Stop container:
"docker stop dataretrieval-local && docker rm dataretrieval-local"

# View logs:
 "docker logs -f dataretrieval-local"

# Test endpoints:"
"curl http://localhost:8080/api/tweets/antisemitic"
"curl http://localhost:8080/api/tweets/not_antisemitic"