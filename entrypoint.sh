#!/bin/sh
set -e

export FLASK_APP=manage:app

echo "Running migrations..."
flask db upgrade

echo "Creating admin user..."
flask create-admin

exec gunicorn -b 0.0.0.0:8000 wsgi:app
