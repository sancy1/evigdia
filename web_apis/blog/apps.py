from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web_apis.blog"
    
    def ready(self):
        # Import and register signals
        from web_apis.blog.models import signals
