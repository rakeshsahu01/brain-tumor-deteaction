FROM node:18-alpine AS client-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client . 
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Copy built React frontend from first stage
COPY --from=client-builder /app/client/build ./client/build

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "--workers", "1", "--worker-class", "sync", "--timeout", "300", "--bind", "0.0.0.0:8000", "app:app"]
