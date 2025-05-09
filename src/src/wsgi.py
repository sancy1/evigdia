

import os

from django.core.wsgi import get_wsgi_application

# Check for a specific environment variable that indicates production (Render)
if 'RENDER' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

application = get_wsgi_application()




# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.src.settings')

# application = get_wsgi_application()
