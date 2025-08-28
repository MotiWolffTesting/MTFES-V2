#!/bin/bash

# OpenShift Deployment Commands (replace placeholders before running)

# Create/select project:
"oc new-project mtfes || oc project mtfes"

# Optional: create Docker Hub pull secret:
"oc create secret docker-registry dockerhub-pull \
  --docker-username=your-dockerhub-username \
  --docker-password=\$DOCKERHUB_TOKEN \
  --docker-email=you@example.com || true"
"oc secrets link default dockerhub-pull --for=pull || true"

# Deploy services (expects KAFKA_BOOTSTRAP_SERVERS, MONGODB_ATLAS_URI, etc. set in env):
"oc new-app your-dockerhub-username/mtfes-retriever:latest --name=retriever \
  -e KAFKA_BOOTSTRAP_SERVERS=\$KAFKA_BOOTSTRAP_SERVERS \
  -e MONGODB_ATLAS_URI=\$MONGODB_ATLAS_URI \
  -e MONGODB_DB_NAME=\$MONGODB_DB_NAME \
  -e MONGODB_COLLECTION_NAME=\$MONGODB_COLLECTION_NAME || true"

"oc new-app your-dockerhub-username/mtfes-preprocessor:latest --name=preprocessor \
  -e KAFKA_BOOTSTRAP_SERVERS=\$KAFKA_BOOTSTRAP_SERVERS || true"

"oc new-app your-dockerhub-username/mtfes-enricher:latest --name=enricher \
  -e KAFKA_BOOTSTRAP_SERVERS=\$KAFKA_BOOTSTRAP_SERVERS || true"

"oc new-app your-dockerhub-username/mtfes-persister:latest --name=persister \
  -e KAFKA_BOOTSTRAP_SERVERS=\$KAFKA_BOOTSTRAP_SERVERS \
  -e MONGODB_URI=\$MONGODB_URI \
  -e MONGODB_DB_NAME=\$MONGODB_DB_NAME || true"

"oc new-app your-dockerhub-username/mtfes-dataretrieval:latest --name=dataretrieval || true"
"oc expose svc/dataretrieval || true"