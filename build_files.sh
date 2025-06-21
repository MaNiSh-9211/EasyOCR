#!/bin/bash
# build_files.sh

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate

echo "Creating cache table..."
python manage.py createcachetable

echo "Build completed successfully!" 