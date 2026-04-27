# Use pre-built React frontend from repository
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies with SSL certificates
RUN apt-get update && apt-get install -y \
    build-essential \
    ca-certificates \
    openssl \
    curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Ensure build directory exists and has proper permissions
RUN mkdir -p client/build && chmod -R 755 client/build

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "--workers", "1", "--worker-class", "sync", "--timeout", "300", "--bind", "0.0.0.0:8000", "app:app"]
