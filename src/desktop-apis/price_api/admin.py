# price_api/admin.py
from django.contrib import admin
from .models import SubscriptionPrice

@admin.register(SubscriptionPrice)
class SubscriptionPriceAdmin(admin.ModelAdmin):
    list_display = ('plan_type', 'price_usd', 'description', 'is_active', 'last_updated')
    list_filter = ('is_active', 'plan_type')
    search_fields = ('plan_type', 'description')  # Include description in search
    list_editable = ('price_usd', 'description', 'is_active') # Make description editable
    readonly_fields = ('last_updated',)