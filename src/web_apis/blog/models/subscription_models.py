

# blog/models/subscription_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


# SUBSCRIPTION ------------------------------------------------------------------------------------------------------
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