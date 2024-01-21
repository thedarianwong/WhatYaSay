#!/bin/bash

IMAGE_NAME="whatyasay-client"
CONTAINER_NAME="whatyasay-client-dev"

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
    if [[ "$(docker ps -q -f name=$CONTAINER_NAME)" ]]; then
        echo "Docker container $CONTAINER_NAME is already running."
    else
        echo "Container $CONTAINER_NAME is not running."
        if [[ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]]; then
            echo "Starting the existing Docker container $CONTAINER_NAME..."
            docker start $CONTAINER_NAME
        else
            echo "Running a new Docker container $CONTAINER_NAME with volume mount..."
            docker run -dp 3000:3000 --name $CONTAINER_NAME -v "$(pwd):/app" $IMAGE_NAME
        fi
    fi
}

# Build and run or start
build_docker_image
run_or_start_docker_container
