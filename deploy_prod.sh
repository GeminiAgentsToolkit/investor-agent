#!/usr/bin/env bash

# Define the file paths
VERSION_FILE="version"
# The start script
PYTHON_FILE="telegram_bot.py"

# Check if the version file exists
if [ ! -f "$VERSION_FILE" ]; then
    echo "Version file not found! Creating one with version 0."
    echo "0" > "$VERSION_FILE"
fi

# Read the current version from the file
VERSION=$(cat "$VERSION_FILE")
echo "Current version: $VERSION"

# Increment the version
NEW_VERSION=$((VERSION + 1))
echo "New version: $NEW_VERSION"

# Update the version in the version file
echo "$NEW_VERSION" > "$VERSION_FILE"

# Detect OS and set sed flag accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_FLAG="-i ''"
else
    SED_FLAG="-i"
fi

# Update the VERSION variable in the Python file
sed $SED_FLAG "s/^VERSION = .*/VERSION = $NEW_VERSION/" "$PYTHON_FILE"

# Define docker names
CONTAINER_NAME="jess_telegram_bot"
IMAGE_NAME="jess_telegram_bot_image"

# Step 1: Stop and Remove the existing container (if it exists)
echo "Stopping existing container..."
docker stop "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"

# Step 2: Build the new image with versioning
echo "Building new Docker image..."
docker build -t "${IMAGE_NAME}:latest" -t "${IMAGE_NAME}:${NEW_VERSION}" .

# Step 2.1: Remove old images, keeping only latest and two previous versions
echo "Cleaning up old Docker images..."
IMAGES_TO_DELETE=$(docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" \
    | grep "${IMAGE_NAME}" \
    | grep -v "latest" \
    | sort -t ':' -k 2 -n -r \
    | awk 'NR>2 {print $2}')

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
    echo "Deployment success! The container is running."
else
    echo "Deployment failed! The container is not running. Check logs for more details."
    docker logs "${CONTAINER_NAME}"
fi
