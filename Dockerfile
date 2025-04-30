# Stage 1: Build Vue.js frontend
FROM node:16 AS frontend-build
WORKDIR /frontend

# Copy the frontend source code
COPY frontend/ .

# Install the dependencies and build the frontend
RUN npm install && npm run build

# Stage 2: Setup Flask backend and combine frontend
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for the backend
WORKDIR /app

# Copy backend requirements and install them
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY backend/ /app

# Copy the built frontend from the first stage to the backend static folder
COPY --from=frontend-build /frontend/dist /app/app/static

#
