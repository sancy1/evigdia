
# blog/admin/analytics_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from web_apis.blog.models.analytics_models import (
    PostView,
    ReadHistory,
    SearchQuery,
    ClickEvent,
    AdminActivityLog
)

@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'user_link',
        'viewer_display',
        'viewed_at_display',
        'time_spent',
        'ip_address'
    )
    list_filter = ('viewed_at', 'post')
    search_fields = (
        'post__title',
        'user__email',
        'ip_address'
    )
    readonly_fields = (
        'post',
        'user',
        'ip_address',
        'user_agent',
        'referrer',
        'viewed_at',
        'time_spent',
        'viewer_display'
    )
    date_hierarchy = 'viewed_at'
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'user',
                'viewer_display'
            )
        }),
        ('Technical', {
            'fields': (
                'ip_address',
                'user_agent',
                'referrer'
            )
        }),
        ('Engagement', {
            'fields': (
                'time_spent',
                'viewed_at'
            )
        })
    )

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "Anonymous"
    user_link.short_description = "User"

    def viewer_display(self, obj):
        if obj.user:
            return f"{obj.user.email} ({obj.ip_address})"
        return f"Anonymous ({obj.ip_address})"
    viewer_display.short_description = "Viewer"

    def viewed_at_display(self, obj):
        return obj.viewed_at.strftime('%Y-%m-%d %H:%M')
    viewed_at_display.short_description = "Viewed At"

@admin.register(ReadHistory)
class ReadHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'user_link',
        'progress_percentage',
        'reading_status',
        'last_read_at_display',
        'is_completed'
    )
    list_filter = ('is_completed', 'post', 'user')
    search_fields = (
        'post__title',
        'user__email'
    )
    readonly_fields = (
        'post',
        'user',
        'last_read_at',
        'read_count',
        'is_completed',
        'scroll_position',
        'progress_percentage',
        'reading_status'
    )
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'user',
                'reading_status',
                'is_completed'
            )
        }),
        ('Progress', {
            'fields': (
                'scroll_position',
                'progress_percentage',
                'read_count'
            )
        }),
        ('Dates', {
            'fields': (
                'last_read_at',
            )
        })
    )

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"

    def user_link(self, obj):
        url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = "User"

    def progress_percentage(self, obj):
        if obj.post.word_count > 0:
            return f"{min(100, (obj.scroll_position / obj.post.word_count) * 100):.1f}%"
        return "0%"
    progress_percentage.short_description = "Progress"

    def reading_status(self, obj):
        if obj.is_completed:
            return "Completed"
        elif obj.scroll_position > 0:
            return "In Progress"
        return "Not Started"
    reading_status.short_description = "Status"

    def last_read_at_display(self, obj):
        return obj.last_read_at.strftime('%Y-%m-%d %H:%M')
    last_read_at_display.short_description = "Last Read"

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = (
        'query',
        'user_link',
        'results_count',
        'created_at_display',
        'ip_address',
        'search_summary'
    )
    list_filter = ('created_at',)
    search_fields = (
        'query',
        'user__email',
        'ip_address'
    )
    readonly_fields = (
        'query',
        'user',
        'ip_address',
        'results_count',
        'created_at',
        'search_summary'
    )
    date_hierarchy = 'created_at'

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "Anonymous"
    user_link.short_description = "User"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Searched At"

    def search_summary(self, obj):
        if obj.user:
            return f"{obj.user.email} searched for '{obj.query}'"
        return f"Anonymous user searched for '{obj.query}'"
    search_summary.short_description = "Summary"

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'user_link',
        'element_type',
        'element_text_preview',
        'created_at_display',
        'click_details_preview'
    )
    list_filter = ('element_type', 'created_at')
    search_fields = (
        'post__title',
        'user__email',
        'element_text',
        'element_id'
    )
    readonly_fields = (
        'post',
        'user',
        'element_type',
        'element_id',
        'element_text',
        'url',
        'ip_address',
        'created_at',
        'click_details'
    )
    date_hierarchy = 'created_at'

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "Anonymous"
    user_link.short_description = "User"

    def element_text_preview(self, obj):
        return obj.element_text[:30] + ("..." if len(obj.element_text) > 30 else "")
    element_text_preview.short_description = "Element Text"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Clicked At"

    def click_details_preview(self, obj):
        details = f"{obj.element_type}: {obj.element_text or obj.element_id}"
        if obj.url:
            details += f" → {obj.url[:30]}..."
        return details
    click_details_preview.short_description = "Click Details"

    def click_details(self, obj):
        details = {
            'element': f"{obj.element_type}: {obj.element_text or obj.element_id}",
            'action': f"Clicked on {obj.element_type} in {obj.post.title}"
        }
        if obj.url:
            details['destination'] = obj.url
        return format_html("<pre>{}</pre>", str(details))
    click_details.short_description = "Details"

@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        'activity_type_display',
        'user_link',
        'post_link',
        'created_at_display',
        'is_processed',
        'activity_details_preview'
    )
    list_filter = (
        'activity_type',
        'is_processed',
        'created_at'
    )
    search_fields = (
        'user__email',
        'post__title',
        'ip_address'
    )
    readonly_fields = (
        'activity_type',
        'user',
        'post',
        'ip_address',
        'metadata_preview',
        'created_at',
        'activity_type_display',
        'activity_details'
    )
    actions = ['mark_as_processed']
    date_hierarchy = 'created_at'

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "System"
    user_link.short_description = "User"

    def post_link(self, obj):
        if obj.post:
            url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', url, obj.post.title)
        return "-"
    post_link.short_description = "Post"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Activity Time"

    def activity_type_display(self, obj):
        return obj.get_activity_type_display()
    activity_type_display.short_description = "Activity Type"

    def activity_details_preview(self, obj):
        details = f"{obj.user.email if obj.user else 'System'} {obj.get_activity_type_display()}"
        if obj.post:
            details += f" on {obj.post.title}"
        return details[:100] + ("..." if len(details) > 100 else "")
    activity_details_preview.short_description = "Activity"

    def activity_details(self, obj):
        details = {
            'type': obj.get_activity_type_display(),
            'action': f"{obj.user.email if obj.user else 'System'} performed {obj.get_activity_type_display()}"
        }
        if obj.post:
            details['post'] = obj.post.title
        return format_html("<pre>{}</pre>", str(details))
    activity_details.short_description = "Full Details"

    def metadata_preview(self, obj):
        return format_html("<pre>{}</pre>", str(obj.metadata))
    metadata_preview.short_description = "Metadata"

    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_as_processed.short_description = "Mark selected as processed"