
# blog/admin/subscription_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from web_apis.blog.models.subscription_models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'email_display',
        'user_link',
        'status_display',
        'subscribed_at_display',
        'unsubscribed_at_display',
        'preferences_short',
        'ip_short'
    )
    list_filter = (
        'is_active',
        'is_confirmed',
        'subscribed_at',
        'unsubscribed_at'
    )
    search_fields = (
        'email',
        'user__email',
        'ip_address'
    )
    readonly_fields = (
        'user',
        'subscribed_at',
        'unsubscribed_at',
        'ip_address',
        'status_display'
    )
    date_hierarchy = 'subscribed_at'
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'user',
                'status_display'
            )
        }),
        ('Status', {
            'fields': (
                'is_active',
                'is_confirmed',
            )
        }),
        ('Preferences', {
            'fields': (
                'preferences',
            )
        }),
        ('Technical', {
            'classes': ('collapse',),
            'fields': (
                'ip_address',
                'confirmation_token',
            )
        }),
        ('Dates', {
            'fields': (
                'subscribed_at',
                'unsubscribed_at',
            )
        })
    )
    actions = [
        'confirm_selected',
        'unconfirm_selected',
        'activate_selected',
        'deactivate_selected'
    ]

    def email_display(self, obj):
        return obj.email
    email_display.short_description = "Email"
    email_display.admin_order_field = 'email'

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "-"
    user_link.short_description = "User"

    def status_display(self, obj):
        if not obj.is_active:
            return format_html('<span style="color: red;">Unsubscribed</span>')
        if obj.is_confirmed:
            return format_html('<span style="color: green;">Confirmed</span>')
        return format_html('<span style="color: orange;">Pending</span>')
    status_display.short_description = "Status"

    def subscribed_at_display(self, obj):
        return obj.subscribed_at.strftime('%Y-%m-%d %H:%M') if obj.subscribed_at else "-"
    subscribed_at_display.short_description = "Subscribed"
    subscribed_at_display.admin_order_field = 'subscribed_at'

    def unsubscribed_at_display(self, obj):
        return obj.unsubscribed_at.strftime('%Y-%m-%d %H:%M') if obj.unsubscribed_at else "-"
    unsubscribed_at_display.short_description = "Unsubscribed"
    unsubscribed_at_display.admin_order_field = 'unsubscribed_at'

    def preferences_short(self, obj):
        return str(obj.preferences)[:50] + ('...' if len(str(obj.preferences)) > 50 else '') if obj.preferences else "-"
    preferences_short.short_description = "Preferences"

    def ip_short(self, obj):
        return obj.ip_address[:15] if obj.ip_address else "-"
    ip_short.short_description = "IP"

    def confirm_selected(self, request, queryset):
        queryset.update(is_confirmed=True)
    confirm_selected.short_description = "Confirm selected subscriptions"

    def unconfirm_selected(self, request, queryset):
        queryset.update(is_confirmed=False)
    unconfirm_selected.short_description = "Unconfirm selected subscriptions"

    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
    activate_selected.short_description = "Activate selected subscriptions"

    def deactivate_selected(self, request, queryset):
        queryset.filter(is_active=True).update(
            is_active=False,
            unsubscribed_at=timezone.now()
        )
    deactivate_selected.short_description = "Deactivate (unsubscribe) selected subscriptions"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')