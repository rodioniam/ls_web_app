#!/bin/sh
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata allocator/fixtures/multipliers.json
gunicorn base.wsgi:application --bind 0.0.0.0:${PORT:-8000}