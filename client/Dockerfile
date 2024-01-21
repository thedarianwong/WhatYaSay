# Use the official lightweight Node.js 16 image.
# https://hub.docker.com/_/node
FROM node:20-alpine

# Set the working directory.
WORKDIR /app

# Copy package.json and package-lock.json (if available).
COPY package*.json ./

# Install project dependencies.
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Bind the app to port 3000.
EXPOSE 3000

# Define the Docker user.
USER node

# Specify the command to run on container start.
CMD ["npm", "run", "dev"]
