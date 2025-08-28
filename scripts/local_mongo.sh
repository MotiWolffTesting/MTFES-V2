#!/bin/bash

# Local MongoDB Commands

# Start MongoDB container:
"docker run -d --name mtfes-mongo -p 27017:27017 -v mtfes-mongo-data:/data/db mongo:6"

# Start existing container:
"docker start mtfes-mongo"

# Stop MongoDB:
"docker stop mtfes-mongo"

# Remove container:
"docker rm mtfes-mongo"

# Check status:
"docker ps | grep mtfes-mongo"

# Connect to MongoDB:
"docker exec -it mtfes-mongo mongosh"
