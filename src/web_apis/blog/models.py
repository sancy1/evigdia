# blog/models.py
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from user_account.models import CustomUser

User = get_user_model()




# --------------------------
# CONTENT ENHANCEMENT MODELS
# --------------------------

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


class CodeSnippet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='code_snippets')
    language = models.CharField(max_length=50)
    code = models.TextField()
    caption = models.CharField(max_length=255, blank=True)
    line_numbers = models.BooleanField(default=True)
    highlighted_lines = models.CharField(max_length=100, blank=True)  # e.g., "1-3,5,7-9"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} snippet in {self.post.title}"


# --------------------------
# NEWSLETTER & SUBSCRIPTIONS
# --------------------------

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='newsletter_subscriptions'
    )
    is_active = models.BooleanField(default=True)
    token = models.CharField(max_length=100, unique=True)
    confirmation_token = models.CharField(max_length=100, blank=True)
    is_confirmed = models.BooleanField(default=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Subscription preferences for categories or post types")
    )

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"Subscription for {self.email} ({'active' if self.is_active else 'inactive'})"


# --------------------------
# CONTENT SYNDICATION
# --------------------------

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



# --------------------------
# SIGNAL HANDLERS
# --------------------------

@receiver(post_save, sender=Comment)
def handle_comment_notification(sender, instance, created, **kwargs):
    if created:
        # Create admin log
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.COMMENT,
            user=instance.user,
            post=instance.post,
            metadata={
                'comment_id': str(instance.id),
                'content_preview': instance.content[:50]
            }
        )
        
        # Create notification for post author if different from commenter
        if instance.user != instance.post.author:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.NotificationType.COMMENT,
                message=f"New comment on your post '{instance.post.title}'",
                target_url=instance.post.get_absolute_url(),
                related_post=instance.post
            )
        
        # Create admin notification
        AdminNotification.create_for_comment(instance)


@receiver(post_save, sender=Like)
def handle_like_notification(sender, instance, created, **kwargs):
    if created:
        # Create admin log
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.LIKE,
            user=instance.user,
            post=instance.post
        )
        
        # Create notification for post author if different from liker
        if instance.user != instance.post.author:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.NotificationType.LIKE,
                message=f"{instance.user.username} liked your post '{instance.post.title}'",
                target_url=instance.post.get_absolute_url(),
                related_post=instance.post
            )


@receiver(post_save, sender=PostReaction)
def handle_reaction_notification(sender, instance, created, **kwargs):
    if created:
        # Create admin notification
        AdminNotification.create_for_reaction(instance)


@receiver(post_save, sender=Favorite)
def handle_favorite_notification(sender, instance, created, **kwargs):
    if created:
        # Create admin log
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.FAVORITE,
            user=instance.user,
            post=instance.post
        )
        
        # Create notification for post author if different from user
        if instance.user != instance.post.author:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.NotificationType.FAVORITE,
                message=f"{instance.user.username} favorited your post '{instance.post.title}'",
                target_url=instance.post.get_absolute_url(),
                related_post=instance.post
            )
        
        # Create admin notification
        AdminNotification.create_for_favorite(instance)


@receiver(post_save, sender=PostView)
def handle_view_notification(sender, instance, created, **kwargs):
    if created:
        # Create admin log
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.POST_VIEW,
            user=instance.user,
            post=instance.post,
            ip_address=instance.ip_address,
            metadata={
                'user_agent': instance.user_agent,
                'referrer': instance.referrer
            }
        )
        
        # Update view count on post
        instance.post.view_count = models.F('view_count') + 1
        instance.post.save(update_fields=['view_count'])
        
        # Create admin notification
        AdminNotification.create_for_post_view(instance)
        
        
        
        
        
        
        
        
        
        