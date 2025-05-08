
#!/bin/bash
set -o errexit

# Explicitly set Python path
export PYTHONPATH="${PYTHONPATH}:/opt/render/project/src"

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate