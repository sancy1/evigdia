

# blog/models/syndication_models.py

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from ..models.blog_models import BlogPost


# SUBSCRIPTION ------------------------------------------------------------------------------------------------------
class ContentSyndication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='syndications')
    platform_name = models.CharField(max_length=100)
    url = models.URLField()
    published_at = models.DateTimeField(null=True, blank=True)
    is_canonical = models.BooleanField(
        default=False,
        help_text=_("Is this the canonical version of the content?")
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Additional metadata about the syndication")
    )

    class Meta:
        verbose_name = _("Content Syndication")
        verbose_name_plural = _("Content Syndications")
        unique_together = ('post', 'platform_name')
        ordering = ['-published_at']

    def __str__(self):
        return f"Syndication of {self.post.title} on {self.platform_name}"