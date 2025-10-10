#!/bin/sh
set -e

export FLASK_APP=wsgi:app
echo "Running migrations..."
flask db upgrade
exec gunicorn -b 0.0.0.0:8000 wsgi:app
