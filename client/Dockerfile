# Use the official lightweight Node.js 16 image.
# https://hub.docker.com/_/node
FROM node:20-alpine

# Create and change to the app directory.
WORKDIR /usr/src/app

# Copy package.json, package-lock.json, and next.config.js files
COPY package*.json ./
COPY next.config.js ./

# Install production dependencies.
RUN npm install --only=production

# Copy local code to the container's work directory.
COPY . ./

# Build the application.
RUN npm run build

# Expose the port the app runs on.
EXPOSE 3000

# Run the application.
CMD ["npm", "start"]
