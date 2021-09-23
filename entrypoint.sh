#!/bin/bash
set -e

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata mydata.json
gunicorn core.wsgi -b 0.0.0.0:8000

exec "$@"
