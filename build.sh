#!/bin/bash
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
if [ "$RENDER" = "true" ]; then
  python manage.py migrate --noinput
fi

# Collect static files
python manage.py collectstatic --noinput