#!/bin/bash
set -o errexit  # Exit on error

# Set Python path for nested structure
export PYTHONPATH="/opt/render/project/src:/opt/render/project/src/src"

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations (only in production)
if [ "$RENDER" = "true" ]; then
  python manage.py migrate --noinput
fi

# Collect static files (if needed)
if [ -f "manage.py" ]; then
  python manage.py collectstatic --noinput
fi