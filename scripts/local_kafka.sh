#!/bin/bash

# Local Kafka Commands

# Start Kafka with Zookeeper (using docker-compose):
"docker-compose up -d kafka zookeeper"

# Or start manually:
"docker run -d --name zookeeper -p 2181:2181 confluentinc/cp-zookeeper:latest"
"docker run -d --name kafka -p 9092:9092 \\"
"  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \\"
"  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \\"
"  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \\"
"  confluentinc/cp-kafka:latest"

# Stop Kafka:
"docker stop kafka zookeeper && docker rm kafka zookeeper"

# Check status:
"docker ps | grep -E '(kafka|zookeeper)'"