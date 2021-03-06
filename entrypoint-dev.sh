#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z social-db 5432; do
  sleep 0.1
done

sleep 1

echo "PostgreSQL started"

python manage.py db upgrade
python manage.py seed-db

flask run --host=0.0.0.0
