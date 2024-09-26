#!/bin/bash

rm .env
ln -s .env.prod .env 

# Define the file paths
VERSION_FILE="version"
PYTHON_FILE="telegram_bot.py"

# Check if the version file exists
if [ ! -f "$VERSION_FILE" ]; then
    echo "Version file not found! Creating one with version 1."
    echo "1" > "$VERSION_FILE"
fi

# Read the current version from the file
VERSION=$(cat "$VERSION_FILE")
echo "Current version: $VERSION"

# Increment the version
NEW_VERSION=$((VERSION + 1))
echo "New version: $NEW_VERSION"

# Update the version in the version file
echo "$NEW_VERSION" > "$VERSION_FILE"

# Update the VERSION variable in the Python file
# Assuming the VERSION variable is on a line like "VERSION = 1" in the Python script
sed -i '' "s/^VERSION = .*/VERSION = $NEW_VERSION/" "$PYTHON_FILE"

echo "Updated version in both the text file and Python script."

# Define variables
CONTAINER_NAME="jess_telegram_bot"
IMAGE_NAME="jess_telegram_bot_image"

# Step 1: Stop and Remove the existing container (if it exists)
echo "Stopping existing container..."
docker stop "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"

# Step 2: Build the new image
echo "Building new Docker image..."
docker build -t "${IMAGE_NAME}" .

# Step 3: Run the new container
echo "Running new container..."
docker run -d --name "${CONTAINER_NAME}" "${IMAGE_NAME}"

echo "Deployment complete!"