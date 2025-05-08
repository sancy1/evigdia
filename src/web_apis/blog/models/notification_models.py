

# blog/models/notification_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ..models.blog_models import BlogPost

User = get_user_model()

# --------------------------
# NOTIFICATION MODELS
# --------------------------

# NOTIFICATION -----------------------------------------------------------------------------------------
class Notification(models.Model):
    class NotificationType(models.TextChoices):
        COMMENT = 'comment', 'New Comment'
        REPLY = 'reply', 'Reply to Comment'
        POST_UPDATE = 'post_update', 'Post Update'
        NEW_POST = 'new_post', 'New Post'
        LIKE = 'like', 'Post Liked'
        FAVORITE = 'favorite', 'Post Favorited'
        VIEW = 'view', 'Post Viewed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    target_url = models.URLField(blank=True)
    related_post = models.ForeignKey(
        BlogPost,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.user.email if self.user else 'system'}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])



# ADMIN NOTIFICATION -----------------------------------------------------------------------------------------
class AdminNotification(models.Model):
    class NotificationType(models.TextChoices):
        POST_VIEW = 'post_view', _('Post View')
        COMMENT = 'comment', _('Comment')
        REACTION = 'reaction', _('Reaction')
        FAVORITE = 'favorite', _('Favorite')
        SEARCH = 'search', _('Search')
        SUBSCRIPTION = 'subscription', _('Subscription')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        help_text=_("Type of notification")
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_object_id = models.UUIDField(null=True, blank=True)
    related_content_type = models.CharField(max_length=100, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _("Admin Notification")
        verbose_name_plural = _("Admin Notifications")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()}: {self.title}"

    @classmethod
    def create_for_post_view(cls, post_view):
        post = post_view.post
        viewer = post_view.user.email if post_view.user else f"Anonymous ({post_view.ip_address})"
        return cls.objects.create(
            notification_type=cls.NotificationType.POST_VIEW,
            title=f"New view on '{post.title}'",
            message=f"{viewer} viewed the post '{post.title}' for {post_view.time_spent} seconds",
            related_object_id=post.id,
            related_content_type='blogpost',
            metadata={
                'post_id': str(post.id),
                'post_title': post.title,
                'viewer': viewer,
                'time_spent': post_view.time_spent,
                'referrer': post_view.referrer,
            }
        )

    @classmethod
    def create_for_comment(cls, comment):
        post = comment.post
        author = comment.display_name
        return cls.objects.create(
            notification_type=cls.NotificationType.COMMENT,
            title=f"New comment on '{post.title}'",
            message=f"{author} commented on '{post.title}': {comment.content[:100]}...",
            related_object_id=comment.id,
            related_content_type='comment',
            metadata={
                'post_id': str(post.id),
                'post_title': post.title,
                'comment_id': str(comment.id),
                'author': author,
                'content_preview': comment.content[:200],
            }
        )

    @classmethod
    def create_for_reaction(cls, reaction):
        post = reaction.post
        user = reaction.user.email
        return cls.objects.create(
            notification_type=cls.NotificationType.REACTION,
            title=f"New reaction on '{post.title}'",
            message=f"{user} reacted with {reaction.get_reaction_display()} to '{post.title}'",
            related_object_id=reaction.id,
            related_content_type='postreaction',
            metadata={
                'post_id': str(post.id),
                'post_title': post.title,
                'user': user,
                'reaction': reaction.reaction,
            }
        )

    @classmethod
    def create_for_favorite(cls, favorite):
        post = favorite.post
        user = favorite.user.email
        return cls.objects.create(
            notification_type=cls.NotificationType.FAVORITE,
            title=f"New favorite on '{post.title}'",
            message=f"{user} added '{post.title}' to favorites",
            related_object_id=favorite.id,
            related_content_type='favorite',
            metadata={
                'post_id': str(post.id),
                'post_title': post.title,
                'user': user,
            }
        )