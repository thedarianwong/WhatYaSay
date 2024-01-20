#!/bin/bash

# Function to start the FastAPI application
start_app() {
    echo "Attempting to start FastAPI application..."
    python3 -m uvicorn main:app --reload
}

# Try to start the app
if ! start_app; then
    echo "Failed to start the application. Attempting to install requirements..."
    # Install requirements from requirements.txt
    python3 -m pip install -r requirements.txt

    # Try to start the app again
    echo "Retrying to start the application..."
    start_app
fi
