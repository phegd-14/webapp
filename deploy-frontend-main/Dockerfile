FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Production image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install serve globally (if not already done on your system)
RUN npm install -g serve

# Copy built application from the builder stage
COPY --from=builder /app/dist ./dist

COPY serve.json ./

# Expose the port serve will use
EXPOSE 3000

# Serve the build output
CMD ["serve", "-s", "dist", "-l", "3000"]