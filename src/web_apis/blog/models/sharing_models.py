

# blog/models/sharing_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ..models.blog_models import BlogPost

User = get_user_model()

# --------------------------
# SOCIAL SHARING MODELS
# --------------------------

# SOCIAL PLATFORM ------------------------------------------------------------------------------------------------------
class SocialPlatform(models.Model):
    """Model for supported social media platforms"""
    name = models.CharField(max_length=50, unique=True)
    base_share_url = models.URLField(help_text="Base URL for sharing (e.g., https://twitter.com/intent/tweet?url=)")
    icon_class = models.CharField(max_length=50, blank=True, help_text="CSS class for platform icon")
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order in sharing widgets")
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name



# SHARE TRACKING ------------------------------------------------------------------------------------------------------
class ShareTracking(models.Model):
    """Tracks shares of content on social media and other platforms"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        BlogPost, 
        on_delete=models.CASCADE, 
        related_name='shares'
    )
    platform = models.ForeignKey(
        SocialPlatform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Null means direct link sharing"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content_shares'
    )
    share_method = models.CharField(
        max_length=20,
        choices=(
            ('social', 'Social Media'),
            ('email', 'Email'),
            ('link', 'Direct Link'),
            ('embed', 'Embedded Share'),
        ),
        default='social'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    referrer = models.URLField(blank=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    clickback_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times people clicked through this share"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional tracking data"
    )

    class Meta:
        ordering = ['-shared_at']
        indexes = [
            models.Index(fields=['post', 'platform']),
            models.Index(fields=['shared_at']),
        ]
        verbose_name = _("Share Tracking")
        verbose_name_plural = _("Share Tracking")

    def __str__(self):
        platform = self.platform.name if self.platform else "Direct"
        return f"Share of {self.post.title} via {platform}"



# SHAREABLE LINK ------------------------------------------------------------------------------------------------------
class ShareableLink(models.Model):
    """Generates and tracks unique shareable links for content"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='shareable_links'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_share_links'
    )
    token = models.CharField(max_length=50, unique=True)
    expiration = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional expiration date for the link"
    )
    max_uses = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Max number of times this link can be used"
    )
    use_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(
        blank=True,
        help_text="Internal notes about this share link"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Shareable Link")
        verbose_name_plural = _("Shareable Links")

    def __str__(self):
        return f"Share link for {self.post.title} ({self.token})"

    @property
    def is_expired(self):
        if self.expiration and timezone.now() > self.expiration:
            return True
        if self.max_uses and self.use_count >= self.max_uses:
            return True
        return not self.is_active

    def get_absolute_url(self):
        return reverse('blog:shared_link', kwargs={'token': self.token})

