#!/bin/bash

# Navigate to the client directory and run stop-dev.sh
echo "Stoping the client..."
cd client
./stop-dev.sh

# Navigate back to the parent directory
cd ..

# Navigate to the server directory and run stop-dev.sh
echo "Stoping the server..."
cd server
./stop-dev.sh
