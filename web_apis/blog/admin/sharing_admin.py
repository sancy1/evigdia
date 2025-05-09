# blog/admin/sharing_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from web_apis.blog.models.sharing_models import SocialPlatform, ShareTracking, ShareableLink

@admin.register(SocialPlatform)
class SocialPlatformAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'base_share_url_short',
        'is_active',
        'order',
        'icon_display'
    )
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'base_share_url')
    fields = (
        'name',
        'base_share_url',
        'icon_class',
        'is_active',
        'order'
    )

    def base_share_url_short(self, obj):
        return obj.base_share_url[:50] + ('...' if len(obj.base_share_url) > 50 else '')
    base_share_url_short.short_description = "Share URL"

    def icon_display(self, obj):
        if obj.icon_class:
            return format_html('<i class="{}"></i> {}', obj.icon_class, obj.icon_class)
        return "-"
    icon_display.short_description = "Icon Preview"
    icon_display.allow_tags = True

@admin.register(ShareTracking)
class ShareTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'platform_link',
        'user_link',
        'share_method_display',
        'shared_at_display',
        'clickback_count',
        'share_details_preview'
    )
    list_filter = (
        'platform',
        'share_method',
        'shared_at'
    )
    search_fields = (
        'post__title',
        'user__email',
        'ip_address'
    )
    readonly_fields = (
        'post',
        'platform',
        'user',
        'share_method',
        'ip_address',
        'user_agent',
        'referrer',
        'shared_at',
        'clickback_count',
        'metadata_display',
        'share_details'
    )
    date_hierarchy = 'shared_at'
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'platform',
                'user',
                'share_method'  # Changed from share_method_display to actual field
            )
        }),
        ('Technical', {
            'classes': ('collapse',),
            'fields': (
                'ip_address',
                'user_agent',
                'referrer',
                'clickback_count'
            )
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': (
                'metadata_display',
                'share_details'
            )
        }),
        ('Dates', {
            'fields': (
                'shared_at',
            )
        })
    )

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"
    post_link.allow_tags = True

    def platform_link(self, obj):
        if obj.platform:
            url = reverse('admin:blog_socialplatform_change', args=[obj.platform.id])
            return format_html('<a href="{}">{}</a>', url, obj.platform.name)
        return "Direct"
    platform_link.short_description = "Platform"
    platform_link.allow_tags = True

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "Anonymous"
    user_link.short_description = "User"
    user_link.allow_tags = True

    def share_method_display(self, obj):
        return obj.get_share_method_display()
    share_method_display.short_description = "Share Method"

    def shared_at_display(self, obj):
        return obj.shared_at.strftime('%Y-%m-%d %H:%M')
    shared_at_display.short_description = "Shared At"

    def share_details_preview(self, obj):
        platform = obj.platform.name if obj.platform else 'Direct'
        user = obj.user.email if obj.user else 'Anonymous'
        return f"{user} via {platform}"
    share_details_preview.short_description = "Share Details"

    def share_details(self, obj):
        details = {
            'platform': obj.platform.name if obj.platform else 'Direct',
            'shared_by': obj.user.email if obj.user else 'Anonymous',
            'content': obj.post.title
        }
        details.update(obj.metadata)
        return format_html("<pre>{}</pre>", str(details))
    share_details.short_description = "Full Details"
    share_details.allow_tags = True

    def metadata_display(self, obj):
        return format_html("<pre>{}</pre>", str(obj.metadata))
    metadata_display.short_description = "Metadata"
    metadata_display.allow_tags = True

@admin.register(ShareableLink)
class ShareableLinkAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'creator_link',
        'token_short',
        'admin_url_link',
        'status',
        'use_count',
        'created_at_display'
    )
    list_filter = (
        'is_active',
        'expiration',
        'created_at'
    )
    search_fields = (
        'post__title',
        'creator__email',
        'token'
    )
    readonly_fields = (
        'post',
        'creator',
        'token',
        'admin_url_link',
        'use_count',
        'created_at',
        'is_expired',
        'status_display'
    )
    actions = ['activate_links', 'deactivate_links']
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'creator',
                'status_display'
            )
        }),
        ('Link Info', {
            'fields': (
                'token',
                'admin_url_link',
                'is_active'
            )
        }),
        ('Usage', {
            'fields': (
                'use_count',
                'max_uses',
            )
        }),
        ('Expiration', {
            'fields': (
                'expiration',
                'is_expired'
            )
        }),
        ('Notes', {
            'fields': (
                'notes',
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
            )
        })
    )

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"
    post_link.allow_tags = True

    def creator_link(self, obj):
        url = reverse('admin:user_account_customuser_change', args=[obj.creator.id])
        return format_html('<a href="{}">{}</a>', url, obj.creator.email)
    creator_link.short_description = "Creator"
    creator_link.allow_tags = True

    def token_short(self, obj):
        return obj.token[:8] + '...' if len(obj.token) > 8 else obj.token
    token_short.short_description = "Token"

    def admin_url_link(self, obj):
        url = reverse('admin:blog_shareablelink_change', args=[obj.id])
        return format_html('<a href="{}">Admin View</a>', url)
    admin_url_link.short_description = "Admin Link"
    admin_url_link.allow_tags = True

    def status(self, obj):
        if not obj.is_active:
            return "Inactive"
        if obj.is_expired:
            return "Expired"
        return "Active"
    status.short_description = "Status"

    def status_display(self, obj):
        if not obj.is_active:
            return format_html('<span style="color: red;">Inactive</span>')
        if obj.is_expired:
            return format_html('<span style="color: orange;">Expired</span>')
        return format_html('<span style="color: green;">Active</span>')
    status_display.short_description = "Status"
    status_display.allow_tags = True

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Created"

    def activate_links(self, request, queryset):
        queryset.update(is_active=True)
    activate_links.short_description = "Activate selected links"

    def deactivate_links(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_links.short_description = "Deactivate selected links"