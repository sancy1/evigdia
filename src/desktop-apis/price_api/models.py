from django.db import models

SUBSCRIPTION_CHOICES = (
    ("monthly", "Monthly"),
    ("yearly", "Yearly"),
)

class SubscriptionPrice(models.Model):
    plan_type = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        unique=True
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in US Dollars"
    )
    description = models.TextField(blank=True, null=True)  # Added description field
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this price is currently active"
    )
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this price is currently active"
    )

    class Meta:
        verbose_name = "Subscription Price"
        verbose_name_plural = "Subscription Prices"

    def __str__(self):
        return f"{self.get_plan_type_display()}: ${self.price_usd}"