# Stage 1: Build React App
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve the React App
FROM node:18-alpine

WORKDIR /app

# Install serve globally
RUN npm install -g serve

# Copy build output
COPY --from=builder /app/dist ./dist

# Copy default config.json to the root of dist/
COPY public/config.json ./dist/config.json

# Expose port
EXPOSE 3000

# Serve the static files
CMD ["serve", "-s", "dist", "-l", "3000"]
