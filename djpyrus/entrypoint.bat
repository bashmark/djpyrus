

echo "Collect static files"
python manage.py collectstatic --no-input

echo "Apply database migrations"
python manage.py makemigrations --no-input
python manage.py migrate --no-input

echo "init admin"
python manage.py init

echo "Starting server"
python manage.py runserver 127.0.0.1:8000