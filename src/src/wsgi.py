

import os
import sys
from django.core.wsgi import get_wsgi_application

# Calculate paths correctly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes up to outer src
PROJECT_DIR = os.path.dirname(BASE_DIR)  # Goes up to project root

# Add both paths to Python path
sys.path.append(BASE_DIR)  # Outer src directory
sys.path.append(PROJECT_DIR)  # Project root

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')  # Changed from src.src.settings

application = get_wsgi_application()







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
