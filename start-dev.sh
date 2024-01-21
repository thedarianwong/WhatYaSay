#!/bin/bash

# Navigate to the client directory and run start-dev.sh
echo "Starting the client..."
cd client
./start-dev.sh

# Navigate back to the parent directory
cd ..

# Navigate to the server directory and run start-dev.sh
echo "Starting the server..."
cd server
./start-dev.sh
