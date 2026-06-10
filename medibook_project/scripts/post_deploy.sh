#!/bin/sh
set -e

# Post-deploy helper: apply migrations, collect static files and create admin user non-interactively
# Usage inside container (Dokploy):
#   DJANGO_ADMIN_USERNAME=admin DJANGO_ADMIN_EMAIL=admin@example.com \
#   DJANGO_ADMIN_PASSWORD=YourPass123 sh /path/to/post_deploy.sh

cd /app/medibook || cd /var/home/medibook || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ -n "$DJANGO_ADMIN_USERNAME" ] && [ -n "$DJANGO_ADMIN_EMAIL" ] && [ -n "$DJANGO_ADMIN_PASSWORD" ]; then
  echo "Creating superuser $DJANGO_ADMIN_USERNAME if not exists..."
  python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
username='${DJANGO_ADMIN_USERNAME}'
email='${DJANGO_ADMIN_EMAIL}'
password='${DJANGO_ADMIN_PASSWORD}'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created')
else:
    print('Superuser already exists')
PY
fi

echo "Post-deploy tasks completed."
