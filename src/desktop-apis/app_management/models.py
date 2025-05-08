from django.db import models
from django.conf import settings

class AppManager(models.Model):
    APP_TYPES = [
        ('general', 'General'),
        ('individual', 'Individual'),
        ('payment', 'Payment'),
        ('user', 'User'),
        ('profile', 'Profile'),
        ('morphpix', 'MorphPix'),
    ]
    
    app_type = models.CharField(max_length=20, choices=APP_TYPES, unique=True)
    is_active = models.BooleanField(default=True)
    requires_update = models.BooleanField(default=False)
    shutdown_message = models.TextField(blank=True, null=True)
    update_message = models.TextField(blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "App Manager"
        verbose_name_plural = "App Managers"
    
    def __str__(self):
        return f"{self.get_app_type_display()} App Manager"

    def save(self, *args, **kwargs):
        if not self.website_url:
            from django.conf import settings
            self.website_url = settings.EVIGDIA_WEBSITE_URL
        super().save(*args, **kwargs)

class GlobalAppControl(models.Model):
    is_global_shutdown = models.BooleanField(default=False)
    global_shutdown_message = models.TextField(blank=True, null=True)
    is_global_update = models.BooleanField(default=False)
    global_update_message = models.TextField(blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Global App Control"
        verbose_name_plural = "Global App Controls"
    
    def __str__(self):
        return "Global App Control Settings"

    def save(self, *args, **kwargs):
        if not self.website_url:
            from django.conf import settings
            self.website_url = settings.EVIGDIA_WEBSITE_URL
        super().save(*args, **kwargs)