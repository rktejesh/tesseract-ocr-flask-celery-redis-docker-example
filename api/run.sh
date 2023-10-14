#!/bin/bash

redis-server & # Start Redis in the background
celery -A app.celery worker --loglevel=info & # Start Celery in the background
python3 app.py # Start your Flask application
# gunicorn --bind 0.0.0.0:5001 --workers 3 app:app