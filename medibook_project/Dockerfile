FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8161

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY medibook /app/medibook
COPY docker-entrypoint.sh /app/

# Normalize Windows line endings and make script executable
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

WORKDIR /app/medibook

# Expose the default Dokploy/Dockplay port. The app still honors $PORT.
EXPOSE 8161

# Run entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]
