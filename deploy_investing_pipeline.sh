#!/usr/bin/env bash

# Define docker names
CONTAINER_NAME="jess_investor_bot"
IMAGE_NAME="jess_investor_bot_image"

# Step 1: Stop and Remove the existing container (if it exists)
echo "Stopping existing container..."
docker stop "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"

# Step 2: Build the new image
echo "Building new Docker image..."

# Get the highest existing sequential tag
PREVIOUS_TAG=$(docker images --format "{{.Tag}}" "${IMAGE_NAME}" \
    | grep -E '^[0-9]+$' \
    | sort -n \
    | tail -n 1)

# Determine the next sequential tag
if [ -z "$PREVIOUS_TAG" ]; then
    NEXT_TAG=0
else
    NEXT_TAG=$((PREVIOUS_TAG + 1))
fi

# Build the new image with both tags: latest and the next sequential number
docker build -t "${IMAGE_NAME}:latest" -t "${IMAGE_NAME}:${NEXT_TAG}" -f Dockerfile.investing_pipeline .

echo "Built new Docker image with tags: latest and ${NEXT_TAG}"

# Step 2.1: Remove old images, keeping only latest and five previous versions
echo "Cleaning up old Docker images..."

IMAGES_TO_DELETE=$(docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" \
    | grep "${IMAGE_NAME}" \
    | grep -v "latest" \
    | sort -t ':' -k 2 -n -r \
    | awk 'NR>5 {print $2}')

if [ -n "$IMAGES_TO_DELETE" ]; then
    echo "Removing old images..."
    docker rmi -f $IMAGES_TO_DELETE
else
    echo "No old images to remove."
fi

# Step 2.1.1: Remove dangling images
echo "Removing dangling images..."
docker image prune -f


# Step 2.2: Check permissions of the sa.json file
SA_FILE="sa.json"
echo "Checking permissions of ${SA_FILE}..."
if [ ! -r "$SA_FILE" ] || [ $(stat -c "%a" "$SA_FILE") -lt 644 ]; then
    echo "Warning: The ${SA_FILE} file must have read permissions for others (at least 644). Setting permissions..."
    chmod 644 "$SA_FILE"
fi

# Step 3: Run the new container
echo "Running new container..."
docker run -d --name "${CONTAINER_NAME}" --env-file $(pwd)/.env.prod -v $(pwd)/sa.json:/app/sa.json:ro "${IMAGE_NAME}:latest"

# Step 4: Check container status
echo "Checking if the container is running..."
STATUS=$(docker inspect -f '{{.State.Running}}' "${CONTAINER_NAME}")
if [ "$STATUS" == "true" ]; then
    echo "Investing pipeline deployment success! The container is running."
else
    echo "Investing pipeline deployment failed! The container is not running. Check logs for more details."
    docker logs "${CONTAINER_NAME}"
fi