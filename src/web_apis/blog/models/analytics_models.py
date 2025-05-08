

# blog/models/analytics_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ..models.blog_models import BlogPost

User = get_user_model()


# POST VIEW ------------------------------------------------------------------------------------------------------
class PostView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_views'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True)
    referrer = models.URLField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(
        default=0,
        help_text=_("Time spent reading in seconds")
    )

    class Meta:
        verbose_name = _("Post View")
        verbose_name_plural = _("Post Views")
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post', 'user']),
            models.Index(fields=['viewed_at']),  # Changed from 'created_at' to 'viewed_at'
        ]

    def __str__(self):
        viewer = self.user.email if self.user else self.ip_address
        return f"View of {self.post.title} by {viewer}"



# READ HISTORY ------------------------------------------------------------------------------------------------------
class ReadHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_read_history')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='read_by')
    last_read_at = models.DateTimeField(auto_now=True)
    read_count = models.PositiveIntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    scroll_position = models.PositiveIntegerField(
        default=0,
        help_text=_("Last scroll position in pixels")
    )

    class Meta:
        verbose_name = _("Read History")
        verbose_name_plural = _("Read Histories")
        unique_together = ('user', 'post')
        ordering = ['-last_read_at']

    def __str__(self):
        return f"{self.user.email}'s reading progress on {self.post.title}"



# ------------------------------------------------------------------------------------------------------
# SEARCH & ANALYTICS MODELS
# --------------------------
class SearchQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_queries'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Search Query")
        verbose_name_plural = _("Search Queries")
        ordering = ['-created_at']

    def __str__(self):
        return f"Search for '{self.query}' by {self.user.email if self.user else 'anonymous'}"



# CLICK EVENT -------------------------------------------------------------------------------------------------------
class ClickEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='click_events')
    element_type = models.CharField(max_length=50)  # e.g., 'internal_link', 'external_link', 'button'
    element_id = models.CharField(max_length=100, blank=True)
    element_text = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_clicks'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Click on {self.element_type} in {self.post.title}"



# -------------------------------------------------------------------------------------------------------
# ADMIN TRACKING MODELS
# --------------------------
class AdminActivityLog(models.Model):
    class ActivityType(models.TextChoices):
        POST_VIEW = 'post_view', 'Post Viewed'
        COMMENT = 'comment', 'Comment Added'
        LIKE = 'like', 'Post Liked'
        DISLIKE = 'dislike', 'Post Disliked'
        FAVORITE = 'favorite', 'Post Favorited'
        SHARE = 'share', 'Post Shared'
        READ = 'read', 'Post Read'
        SEARCH = 'search', 'Content Searched'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities'
    )
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['activity_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_processed']),
        ]

    def __str__(self):
        return f"{self.get_activity_type_display()} by {self.user.email if self.user else 'anonymous'}"

    def process(self):
        """Mark activity as processed by admin"""
        self.is_processed = True
        self.save(update_fields=['is_processed'])


