#!/bin/bash

# Define variables
CONTAINER_NAME="jess_investor_bot"
IMAGE_NAME="jess_investor_bot_image"

# Step 1: Stop and Remove the existing container (if it exists)
echo "Stopping existing container..."
docker stop "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"

# Step 2: Build the new image
echo "Building new Docker image..."
# Dockerfile is Dockerfile.investing_pipeline
docker build -t "${IMAGE_NAME}" -f Dockerfile.investing_pipeline .

# Step 3: Run the new container
echo "Running new container..."
docker run -d --name "${CONTAINER_NAME}" "${IMAGE_NAME}"

echo "Deployment complete!"