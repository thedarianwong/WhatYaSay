#!/bin/bash

CONTAINER_NAME="fastapi_container"

# Function to stop the Docker container
stop_docker_container() {
    echo "Stopping Docker container $CONTAINER_NAME..."
    if [[ "$(docker ps -q -f name=$CONTAINER_NAME)" ]]; then
        docker stop $CONTAINER_NAME
        echo "Container $CONTAINER_NAME stopped."
    else
        echo "No running container found with name $CONTAINER_NAME."
    fi
}

# Stop the container
stop_docker_container

# Additional commands for manual cleanup or full rebuild:

# To remove the container (if stopped):
# docker rm $CONTAINER_NAME

# To remove the Docker image:
# docker rmi fastapi_app

# To rebuild the Docker image from scratch (useful after significant changes):
# docker build -t fastapi_app --no-cache .

# Note: Removing images and containers is irreversible. Ensure you have backups of necessary data before performing these actions.
