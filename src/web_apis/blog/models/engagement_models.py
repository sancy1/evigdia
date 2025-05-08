
# blog/models/engagement_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from ..models.blog_models import BlogPost

User = get_user_model()


# --------------------------
# USER ENGAGEMENT MODELS
# --------------------------

# COMMENT -----------------------------------------------------------------------------------------
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # For anonymous comments
    author_name = models.CharField(max_length=100, blank=True)
    author_email = models.EmailField(blank=True)
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    
    content = models.TextField(max_length=1000, validators=[MinLengthValidator(10)])
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    referrer = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['is_approved']),
            models.Index(fields=['created_at']),
        ]
        permissions = [
            ('can_moderate', 'Can moderate comments'),
        ]

    def __str__(self):
        return f"Comment by {self.display_name} on {self.post.title}"

    @property
    def display_name(self):
        if self.user:
            return self.user.get_full_name()
        return self.author_name or self.guest_name

    @property
    def author_email(self):
        return self.user.email if self.user else self.guest_email

    @property
    def is_reply(self):
        return self.parent is not None

    def approve(self):
        self.is_approved = True
        self.save(update_fields=['is_approved'])



# COMMENT REACTION -----------------------------------------------------------------------------------------
class CommentReaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = 'like', _('Like')
        DISLIKE = 'dislike', _('Dislike')
        LAUGH = 'laugh', _('Laugh')
        HEART = 'heart', _('Heart')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reactions')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=10, choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Comment Reaction")
        verbose_name_plural = _("Comment Reactions")
        unique_together = ('user', 'comment')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} reacted with {self.get_reaction_display()} to comment {self.comment.id}"



# LIKE -----------------------------------------------------------------------------------------
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_likes')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} likes {self.post.title}"



# POST REACTION -----------------------------------------------------------------------------------------
class PostReaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = 'like', _('Like')
        LOVE = 'love', _('Love')
        LAUGH = 'laugh', _('Laugh')
        WOW = 'wow', _('Wow')
        SAD = 'sad', _('Sad')
        ANGRY = 'angry', _('Angry')
        THUMBS_UP = 'thumbs_up', _('Thumbs Up')
        THUMBS_DOWN = 'thumbs_down', _('Thumbs Down')
        CHECKMARK = 'checkmark', _('Checkmark')
        STAR = 'star', _('Star')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_reactions')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=20, choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Post Reaction")
        verbose_name_plural = _("Post Reactions")
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} reacted with {self.get_reaction_display()} to {self.post.title}"



# FAVORITE -----------------------------------------------------------------------------------------
class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_favorites')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text=_("Optional notes about why this was favorited"))

    class Meta:
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")
        unique_together = ('user', 'post')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} favorited {self.post.title}"