
# blog/admin/syndication_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from web_apis.blog.models.syndication_models import ContentSyndication

@admin.register(ContentSyndication)
class ContentSyndicationAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'platform_name_display',
        'url_short',
        'published_at_display',
        'canonical_status',
        'metadata_preview'
    )
    list_filter = (
        'platform_name',
        'is_canonical',
        'published_at'
    )
    search_fields = (
        'post__title',
        'platform_name',
        'url'
    )
    readonly_fields = (
        'post',
        'platform_details_display',
        'metadata_display'
    )
    date_hierarchy = 'published_at'
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'platform_name',
                'platform_details_display'
            )
        }),
        ('Syndication Details', {
            'fields': (
                'url',
                'published_at',
                'is_canonical'
            )
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': (
                'metadata_display',
            )
        })
    )
    actions = [
        'mark_as_canonical',
        'unmark_as_canonical',
        'update_published_now'
    ]

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"
    post_link.admin_order_field = 'post__title'

    def platform_name_display(self, obj):
        return obj.platform_name.title()
    platform_name_display.short_description = "Platform"
    platform_name_display.admin_order_field = 'platform_name'

    def url_short(self, obj):
        if obj.url:
            return format_html(
                '<a href="{}" target="_blank">{}...</a>',
                obj.url,
                obj.url[:30]
            )
        return "-"
    url_short.short_description = "URL"

    def published_at_display(self, obj):
        if obj.published_at:
            return obj.published_at.strftime('%Y-%m-%d %H:%M')
        return "Not published"
    published_at_display.short_description = "Published At"
    published_at_display.admin_order_field = 'published_at'

    def canonical_status(self, obj):
        if obj.is_canonical:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Canonical</span>'
            )
        return format_html(
            '<span style="color: #666;">Mirror</span>'
        )
    canonical_status.short_description = "Status"

    def metadata_preview(self, obj):
        if obj.metadata:
            return str(obj.metadata)[:50] + ('...' if len(str(obj.metadata)) > 50 else '')
        return "-"
    metadata_preview.short_description = "Metadata Preview"

    def platform_details_display(self, obj):
        details = {
            'platform': obj.platform_name,
            'url': obj.url,
            'is_canonical': obj.is_canonical,
            'published_at': obj.published_at.strftime('%Y-%m-%d %H:%M:%S') if obj.published_at else None
        }
        return format_html("<pre>{}</pre>", str(details))
    platform_details_display.short_description = "Platform Details"

    def metadata_display(self, obj):
        return format_html("<pre>{}</pre>", str(obj.metadata))
    metadata_display.short_description = "Full Metadata"

    def mark_as_canonical(self, request, queryset):
        # Ensure only one canonical per platform per post
        for syndication in queryset:
            ContentSyndication.objects.filter(
                post=syndication.post,
                platform_name=syndication.platform_name
            ).update(is_canonical=False)
            syndication.is_canonical = True
            syndication.save()
        self.message_user(request, f"Marked {queryset.count()} syndications as canonical")
    mark_as_canonical.short_description = "Mark selected as canonical"

    def unmark_as_canonical(self, request, queryset):
        queryset.update(is_canonical=False)
        self.message_user(request, f"Unmarked {queryset.count()} canonical syndications")
    unmark_as_canonical.short_description = "Unmark selected as canonical"

    def update_published_now(self, request, queryset):
        queryset.filter(published_at__isnull=True).update(published_at=timezone.now())
        self.message_user(request, f"Set publish date to now for {queryset.count()} syndications")
    update_published_now.short_description = "Set publish date to now"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')