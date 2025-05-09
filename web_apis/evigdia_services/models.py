# web_apis/evigdia_services/models.py

import os
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _



def upload_service_file_path(instance, filename):
    """Generates a unique file path for service attachments."""
    today = timezone.now()
    return f"service_files/{today.year}/{today.month}/{today.day}/{uuid.uuid4()}_{filename}"


class Service(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    # Main content fields
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    sub_description = models.TextField(blank=True, null=True)
    
    # Images
    service_image = models.ImageField(upload_to='services/', blank=True, null=True)
    sub_service_image = models.ImageField(upload_to='sub_services/', blank=True, null=True)
    
    # Metadata
    date_posted = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Relationships
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_services'
    )

    class Meta:
        ordering = ['-date_posted']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


    #  SEO and slug
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    canonical_url = models.URLField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        # Set meta fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description and self.description:
            self.meta_description = self.description[:160]
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('service-detail', kwargs={'slug': self.slug})


class ServiceAttachment(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='attachments',
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=upload_service_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'xls', 'xlsx', 'ppt', 'pptx']
            )
        ],
        blank=True,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.file.name)

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        return os.path.splitext(self.file.name)[1][1:].lower()

    def filesize(self):
        return self.file.size if self.file else 0

    class Meta:
        verbose_name = "Service Attachment"
        verbose_name_plural = "Service Attachments"