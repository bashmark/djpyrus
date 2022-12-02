#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --no-input

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "init admin"
python manage.py init

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000