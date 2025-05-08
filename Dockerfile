FROM node:20-alpine AS frontend-builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json yarn.lock* ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy all files
COPY . .

# Build the Next.js application
RUN yarn build

# Production image
FROM python:3.9-slim AS production

# Install system dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the built Next.js app
COPY --from=frontend-builder /app/.next ./.next
COPY --from=frontend-builder /app/node_modules ./node_modules
COPY --from=frontend-builder /app/public ./public
COPY --from=frontend-builder /app/package.json ./package.json
COPY --from=frontend-builder /app/next.config.js ./next.config.js

# Copy Python files and requirements
COPY requirements.txt server.py yolov8n.pt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for both Next.js and Flask
EXPOSE 3000 5000

# Start both servers
CMD ["sh", "-c", "python server.py & yarn start"]
