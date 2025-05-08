# blog/admin/notification_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.apps import apps
import json
from web_apis.blog.models.notification_models import Notification, AdminNotification
from user_account.models import CustomUser

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'notification_type_display',
        'user_link',
        'message_preview',
        'is_read',
        'created_at_display',
        'related_post_link'
    )
    list_filter = (
        'notification_type',
        'is_read',
        'created_at'
    )
    search_fields = (
        'message',
        'user__email',
        'related_post__title'
    )
    readonly_fields = (
        'user',
        'notification_type',
        'message',
        'target_url',
        'related_post',
        'created_at',
        'notification_type_display',
        'time_since_created'
    )
    actions = ['mark_as_read', 'mark_as_unread']
    list_select_related = ('user', 'related_post')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'notification_type_display',
                'is_read'
            )
        }),
        ('Content', {
            'fields': (
                'message',
                'target_url',
                'related_post'
            )
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': (
                'created_at',
                'time_since_created'
            )
        })
    )

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "System"
    user_link.short_description = "User"
    user_link.allow_tags = True

    def message_preview(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    message_preview.short_description = "Message"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Created"

    def notification_type_display(self, obj):
        return obj.get_notification_type_display()
    notification_type_display.short_description = "Type"

    def related_post_link(self, obj):
        if obj.related_post:
            url = reverse('admin:blog_blogpost_change', args=[obj.related_post.id])
            return format_html('<a href="{}">{}</a>', url, obj.related_post.title)
        return "-"
    related_post_link.short_description = "Post"
    related_post_link.allow_tags = True

    def time_since_created(self, obj):
        return obj.created_at.timesince()
    time_since_created.short_description = "Time Since"

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'notification_type_display',
        'title_preview',
        'is_read',
        'created_at_display',
        'related_object_link'
    )
    list_filter = (
        'notification_type',
        'is_read',
        'created_at'
    )
    search_fields = (
        'title',
        'message',
        'related_content_type'
    )
    readonly_fields = (
        'notification_type',
        'title',
        'message',
        'related_object_id',
        'related_content_type',
        'created_at',
        'metadata_preview',
        'notification_type_display',
        'time_since_created'
    )
    actions = ['mark_as_read', 'mark_as_unread']
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': (
                'notification_type_display',
                'is_read'
            )
        }),
        ('Content', {
            'fields': (
                'title',
                'message',
            )
        }),
        ('Related Object', {
            'fields': (
                'related_content_type',
                'related_object_id',
            )
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': (
                'metadata_preview',
                'created_at',
                'time_since_created'
            )
        })
    )

    def title_preview(self, obj):
        return obj.title[:50] + ("..." if len(obj.title) > 50 else "")
    title_preview.short_description = "Title"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Created"

    def notification_type_display(self, obj):
        return obj.get_notification_type_display()
    notification_type_display.short_description = "Type"

    def related_object_link(self, obj):
        if obj.related_content_type and obj.related_object_id:
            try:
                model = apps.get_model('blog', obj.related_content_type)
                if model:  # Check if model exists
                    related_obj = model.objects.filter(pk=obj.related_object_id).first()
                    if related_obj:
                        url = reverse(f'admin:blog_{obj.related_content_type}_change', 
                                    args=[obj.related_object_id])
                        return format_html('<a href="{}">{}</a>', url, str(related_obj))
            except (LookupError, AttributeError):
                pass
            return f"{obj.related_content_type} #{obj.related_object_id}"
        return "-"
    related_object_link.short_description = "Related Object"
    related_object_link.allow_tags = True

    def metadata_preview(self, obj):
        try:
            return format_html("<pre>{}</pre>", json.dumps(obj.metadata, indent=2))
        except (TypeError, ValueError):
            return "Invalid metadata format"
    metadata_preview.short_description = "Metadata"
    metadata_preview.allow_tags = True

    def time_since_created(self, obj):
        return obj.created_at.timesince()
    time_since_created.short_description = "Time Since"

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()