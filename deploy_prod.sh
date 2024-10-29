#!/usr/bin/env bash

# Check if there are uncommitted changes (both staged and unstaged)
# Ensure no uncommitted changes are present before deployment
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "Uncommitted changes detected. Deployment is not allowed without committing all changes."
    exit 1
fi

# Get branch name and commit hash
# Extract the branch name, convert to lowercase, and replace non-alphanumeric characters with underscores
# This ensures the tag is Docker-compatible
git_branch=$(git rev-parse --abbrev-ref HEAD | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g')
git_commit=$(git rev-parse --short HEAD)

echo "Branch: $git_branch"
echo "Commit: $git_commit"

# Write version information to version file
cat <<EOF > ./version
Branch: $git_branch
Commit: $git_commit
Date: $(date +"%Y-%m-%d %H:%M:%S")
Author: $(git log -1 --pretty=format:'%an')
Message: $(git log -1 --pretty=%B)
EOF

echo "Version information written to ./version."

# Define Docker container and image names
CONTAINER_NAME="jess_telegram_bot"
IMAGE_NAME="jess_telegram_bot_image"

# Stop and remove existing container if present
echo "Stopping existing container..."
docker stop "${CONTAINER_NAME}" 2>/dev/null || true
docker rm "${CONTAINER_NAME}" 2>/dev/null || true

# Build the new Docker image
echo "Building new Docker image..."
docker build -t "${IMAGE_NAME}:latest" -t "${IMAGE_NAME}:${git_branch}_${git_commit}" .

# Remove old images, keeping only latest and six previous versions
echo "Cleaning up old Docker images..."
docker images --format "{{.Repository}}:{{.Tag}}" \
    | grep "${IMAGE_NAME}" \
    | sort -t ':' -k 2 -n -r \
    | awk 'NR>7 {print $1":"$2}' \
    | xargs -r docker rmi -f

# Remove dangling images (untagged)
echo "Removing dangling images..."
docker image prune -f

# Check permissions of the sa.json file
# Ensure that the service account file has appropriate read permissions
SA_FILE="sa.json"
echo "Checking permissions of ${SA_FILE}..."
if [ ! -r "$SA_FILE" ] || [ $(stat -c "%a" "$SA_FILE") -lt 644 ]; then
    echo "Setting appropriate permissions for ${SA_FILE}..."
    chmod 644 "$SA_FILE"
fi

# Run the new container
echo "Running new container..."
docker run -d --name "${CONTAINER_NAME}" \
    --env-file "$(pwd)/.env.prod" \
    -v "$(pwd)/sa.json:/app/sa.json:ro" \
    -v "$(pwd)/version:/app/version:ro" \
    "${IMAGE_NAME}:latest"

# Check container status with retries
echo "Checking if the container is running..."
attempts=5
sleep_time=2
sleep $sleep_time
for ((i=1; i<=attempts; i++)); do
    STATUS=$(docker inspect -f '{{.State.Status}}' "${CONTAINER_NAME}" 2>/dev/null)
    if [ "$STATUS" == "running" ]; then
        echo "Deployment success! The container is running."
        exit 0
    else
        echo "Attempt $i/$attempts: Container is not running. Retrying in $sleep_time seconds..."
    fi
    sleep $sleep_time
done

# Output logs for debugging if the container fails to start
echo "Deployment failed! The container did not start in time. Check logs for more details."
docker logs "${CONTAINER_NAME}"
exit 1
