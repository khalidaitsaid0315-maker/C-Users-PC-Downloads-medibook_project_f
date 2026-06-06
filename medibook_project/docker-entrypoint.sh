#!/bin/bash
set -e

PORT="${PORT:-8161}"

if [ "${DB_ENGINE:-sqlite}" = "postgres" ]; then
    echo "Waiting for PostgreSQL at ${DB_HOST:-db}:${DB_PORT:-5432}..."
    until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}"; do
        sleep 2
    done
fi

echo "Running Django migrations..."
cd /app/medibook
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn on port ${PORT}..."
exec gunicorn medibook.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers 4 \
    --worker-class sync \
    --max-requests 1000 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
