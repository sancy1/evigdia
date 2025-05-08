# blog/admin/content_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from web_apis.blog.models.content_models import MediaAttachment, CodeSnippet

@admin.register(MediaAttachment)
class MediaAttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'preview_thumbnail',  # Added this method below
        'post_link',
        'media_type_display',
        'caption_short',
        'created_by_link',
        'created_at_display',
        'file_url_link'
    )
    list_filter = (
        'media_type',
        'created_at'
    )
    search_fields = (
        'post__title',
        'caption',
        'created_by__email'
    )
    readonly_fields = (
        'created_at',
        'created_by',
        'media_type_display',
        'file_preview',
        'file_url_display'
    )
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'created_by',
                'media_type_display'
            )
        }),
        ('Content', {
            'fields': (
                'upload',
                'url',
                'file_preview',
                'file_url_display'
            )
        }),
        ('Metadata', {
            'fields': (
                'caption',
                'alt_text'
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
            )
        })
    )

    def preview_thumbnail(self, obj):  # Added this missing method
        if obj.upload and obj.media_type == 'image':
            return format_html('<img src="{}" height="50" />', obj.upload.url)
        elif obj.url and obj.media_type == 'image':
            return format_html('<img src="{}" height="50" />', obj.url)
        return "-"
    preview_thumbnail.short_description = "Preview"
    preview_thumbnail.allow_tags = True

    def post_link(self, obj):
        if obj.post:
            url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', url, obj.post.title)
        return "-"
    post_link.short_description = "Post"

    def created_by_link(self, obj):
        if obj.created_by:
            url = reverse('admin:user_account_customuser_change', args=[obj.created_by.id])
            return format_html('<a href="{}">{}</a>', url, obj.created_by.email)
        return "-"
    created_by_link.short_description = "Created By"

    def media_type_display(self, obj):
        return obj.get_media_type_display()
    media_type_display.short_description = "Type"

    def caption_short(self, obj):
        return obj.caption[:30] + ("..." if len(obj.caption) > 30 else "") if obj.caption else "-"
    caption_short.short_description = "Caption"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Created"

    def file_url_link(self, obj):
        if obj.upload:
            return format_html('<a href="{}">Download</a>', obj.upload.url)
        elif obj.url:
            return format_html('<a href="{}" target="_blank">View</a>', obj.url)
        return "-"
    file_url_link.short_description = "File"
    file_url_link.allow_tags = True

    def file_preview(self, obj):
        if obj.upload and obj.media_type == 'image':
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.upload.url)
        elif obj.url and obj.media_type == 'image':
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.url)
        return "Preview not available"
    file_preview.short_description = "Preview"
    file_preview.allow_tags = True

    def file_url_display(self, obj):
        if obj.upload:
            return obj.upload.url
        return obj.url if obj.url else "-"
    file_url_display.short_description = "File URL"

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'language',
        'caption_short',
        'line_numbers_display',
        'highlighted_lines_short',
        'created_at_display'
    )
    list_filter = (
        'language',
        'line_numbers',
        'created_at'
    )
    search_fields = (
        'post__title',
        'language',
        'caption',
        'code'
    )
    readonly_fields = (
        'created_at',
        'code_preview',
        'highlighted_lines_display'
    )
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'language'
            )
        }),
        ('Code', {
            'fields': (
                'code',
                'code_preview'
            )
        }),
        ('Display', {
            'fields': (
                'caption',
                'line_numbers',
                'highlighted_lines',
                'highlighted_lines_display'
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

    def caption_short(self, obj):
        return obj.caption[:30] + ("..." if len(obj.caption) > 30 else "") if obj.caption else "-"
    caption_short.short_description = "Caption"

    def line_numbers_display(self, obj):
        return "✓" if obj.line_numbers else "✗"
    line_numbers_display.short_description = "Line Numbers"
    line_numbers_display.allow_tags = True

    def highlighted_lines_short(self, obj):
        return obj.highlighted_lines[:20] + ("..." if len(obj.highlighted_lines) > 20 else "") if obj.highlighted_lines else "-"
    highlighted_lines_short.short_description = "Highlighted"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_display.short_description = "Created"

    def code_preview(self, obj):
        return format_html("<pre>{}</pre>", obj.code[:500] + ("..." if len(obj.code) > 500 else ""))
    code_preview.short_description = "Code Preview"
    code_preview.allow_tags = True

    def highlighted_lines_display(self, obj):
        if obj.highlighted_lines:
            return format_html("<pre>{}</pre>", obj.highlighted_lines)
        return "-"
    highlighted_lines_display.short_description = "Highlighted Lines Preview"
    highlighted_lines_display.allow_tags = True