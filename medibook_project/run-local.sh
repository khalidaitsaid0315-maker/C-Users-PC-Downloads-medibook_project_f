#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found. Install Docker and Docker Compose first."
  exit 2
fi

# Ensure .env exists
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
    echo ".env created from .env.example. Edit .env to set SECRET_KEY and DB_PASSWORD before running in production."
  else
    echo "No .env or .env.example found. Create a .env file before continuing." >&2
  fi
fi

echo "Building and starting containers (detached)..."
docker compose up -d --build

echo "Waiting a few seconds for services to initialize..."
sleep 5

echo "Tailing web logs (CTRL+C to exit)..."
docker compose logs -f web
