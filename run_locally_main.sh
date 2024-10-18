#!/usr/bin/env bash

# Configuration
LOG_FILE="script.log"
GOOGLE_CREDENTIALS_PATH="./sa.json"

# Function to disconnect VPN and clear ENV upon exit
cleanup() {
    # Clear ENV
    unset GOOGLE_APPLICATION_CREDENTIALS
    exit
}

# Signal handling for proper script termination
trap cleanup SIGINT SIGTERM

# Redirect script output to log file and terminal
exec > >(tee -a "$LOG_FILE") 2>&1

# Check for the presence of sa.json file
if [ ! -f "$GOOGLE_CREDENTIALS_PATH" ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] File $GOOGLE_CREDENTIALS_PATH not found."
    cleanup
fi

# Set up ENV
export GOOGLE_APPLICATION_CREDENTIALS="$GOOGLE_CREDENTIALS_PATH"
echo "[$(date +"%Y-%m-%d %H:%M:%S")] GOOGLE_APPLICATION_CREDENTIALS variable is set."

# Check for the presence of main.py
if [ ! -f "main.py" ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] File main.py not found."
    cleanup
fi

# Run the application
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Running main.py..."
python3 main.py

# Check if main.py executed successfully
if [ $? -ne 0 ]; then
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Application main.py terminated with an error."
    cleanup
else
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Application main.py completed successfully."
fi

# Clear ENV after completion
cleanup
