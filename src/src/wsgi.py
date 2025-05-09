

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the directory containing your top-level packages to sys.path, specifically 'src'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up two levels from wsgi.py
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))  # Add the outer 'src' to sys.path

# Set the Django settings module
if 'RENDER' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')  # Production on Render
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')  # Local development

application = get_wsgi_application()

# Optional:  Verify the path (for debugging)
# print(f"sys.path after modification: {sys.path}")






# import os

# from django.core.wsgi import get_wsgi_application

# # Check for a specific environment variable that indicates production (Render)
# if 'RENDER' in os.environ:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

# application = get_wsgi_application()




# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')

# application = get_wsgi_application()
