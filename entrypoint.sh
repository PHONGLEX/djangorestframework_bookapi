#!/bin/bash
set -e

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata mydata.json
python manage.py collectstatic --noinput
gunicorn core.wsgi -b 0.0.0.0:8000


exec "$@"
