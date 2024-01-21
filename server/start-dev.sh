#!/bin/bash

IMAGE_NAME="fastapi_app"
CONTAINER_NAME="fastapi_container"

# Function to build Docker image if it doesn't exist
build_docker_image() {
    echo "Checking if Docker image $IMAGE_NAME exists..."
    if [[ "$(docker images -q $IMAGE_NAME:latest 2> /dev/null)" == "" ]]; then
        echo "Image doesn't exist. Building Docker image..."
        docker build -t $IMAGE_NAME .
    else
        echo "Docker image $IMAGE_NAME already exists."
    fi
}

# Function to run or start Docker container with volume mount for development
run_or_start_docker_container() {
    echo "Checking if Docker container $CONTAINER_NAME is running..."
    # Check if the container is running
    if [[ "$(docker ps -q -f name=$CONTAINER_NAME)" ]]; then
        echo "Docker container $CONTAINER_NAME is already running."
    else
        echo "Container $CONTAINER_NAME is not running."
        # Check if the container exists (created or stopped)
        if [[ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]]; then
            echo "Starting the existing Docker container $CONTAINER_NAME..."
            docker start $CONTAINER_NAME
        else
            echo "Running a new Docker container $CONTAINER_NAME with volume mount..."
            docker run -p 8000:8000 --name $CONTAINER_NAME -v $(pwd):/app $IMAGE_NAME
        fi
    fi
}

# Build and run or start
build_docker_image
run_or_start_docker_container

# Instructions for manual cleanup or rebuild:
# To stop and remove the container: docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
# To remove the Docker image: docker rmi $IMAGE_NAME
# To force rebuild the image: docker build -t $IMAGE_NAME --no-cache .
