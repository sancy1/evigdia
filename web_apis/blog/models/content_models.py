

# blog/models/content_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ..models.blog_models import BlogPost

User = get_user_model()


# MEDIA ATTACHMENT ------------------------------------------------------------------------------------------------------
class MediaAttachment(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        DOCUMENT = 'document', 'Document'
        AUDIO = 'audio', 'Audio'
        EMBED = 'embed', 'Embed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='media_attachments',
        null=True,
        blank=True
    )
    upload = models.FileField(
        upload_to='blog/media/%Y/%m/',
        null=True,
        blank=True
    )
    url = models.URLField(blank=True)
    media_type = models.CharField(
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.IMAGE
    )
    caption = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(max_length=125, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_media_type_display()} attachment for {self.post.title if self.post else 'unattached'}"



# CODE SNIPPET ------------------------------------------------------------------------------------------------------
class CodeSnippet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='code_snippets')
    language = models.CharField(max_length=50)
    code = models.TextField()
    caption = models.CharField(max_length=255, blank=True)
    line_numbers = models.BooleanField(default=True)
    highlighted_lines = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} snippet in {self.post.title}"