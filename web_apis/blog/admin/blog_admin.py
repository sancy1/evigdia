# blog/admin/blog_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from web_apis.blog.models import Category, Tag, BlogPost, BlogPostRevision

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at', 'admin_view_link')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'admin_view_link')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active')
        }),
        ('Content', {
            'fields': ('description', 'icon')
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'admin_view_link')
        })
    )

    def admin_view_link(self, obj):
        url = reverse('admin:blog_category_change', args=[obj.id])
        return format_html('<a href="{}">Edit in Admin</a>', url)
    admin_view_link.short_description = "Admin Link"
    admin_view_link.allow_tags = True

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

class BlogPostRevisionInline(admin.TabularInline):
    model = BlogPostRevision
    extra = 0
    readonly_fields = ('revision_number', 'title', 'updated_by', 'created_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'status',
        'is_featured',
        'is_pinned',
        'published_at',
        'view_count',
        'admin_view_link'
    )
    list_filter = (
        'status',
        'is_featured',
        'is_pinned',
        'categories',
        'published_at'
    )
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = (
        'created_at',
        'updated_at',
        'view_count',
        'comment_count',
        'like_count',
        'reading_time',
        'word_count',
        'admin_view_link',
        'rendered_content_preview'
    )
    raw_id_fields = ('author', 'related_posts')
    filter_horizontal = ('categories', 'tags')
    date_hierarchy = 'published_at'
    inlines = (BlogPostRevisionInline,)
    actions = ['make_published', 'make_draft']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Content', {
            'fields': (
                'excerpt',
                'content',
                'rendered_content_preview',
                'featured_image',
                'featured_image_alt',
                'embedded_media'
            )
        }),
        ('Metadata', {
            'fields': (
                'categories',
                'tags',
                'related_posts',
                'code_snippets_data'
            )
        }),
        ('Settings', {
            'fields': (
                'is_featured',
                'is_pinned',
                'allow_comments',
                'reading_time'
            )
        }),
        ('SEO', {
            'classes': ('collapse',),
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url'
            )
        }),
        ('Statistics', {
            'classes': ('collapse',),
            'fields': (
                'view_count',
                'comment_count',
                'like_count',
                'word_count'
            )
        }),
        ('Dates', {
            'fields': (
                'published_at',
                'scheduled_at',
                'created_at',
                'updated_at'
            )
        }),
        ('Admin Links', {
            'classes': ('collapse',),
            'fields': ('admin_view_link',)
        })
    )

    def admin_view_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.id])
        return format_html('<a href="{}">Edit in Admin</a>', url)
    admin_view_link.short_description = "Admin Link"
    admin_view_link.allow_tags = True

    def rendered_content_preview(self, obj):
        return format_html(obj.rendered_content[:500] + "...")
    rendered_content_preview.short_description = "Content Preview"

    def make_published(self, request, queryset):
        queryset.update(status=BlogPost.PostStatus.PUBLISHED)
    make_published.short_description = "Mark selected posts as published"

    def make_draft(self, request, queryset):
        queryset.update(status=BlogPost.PostStatus.DRAFT)
    make_draft.short_description = "Mark selected posts as draft"

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(BlogPostRevision)
class BlogPostRevisionAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'revision_number',
        'title',
        'updated_by',
        'created_at'
    )
    list_filter = ('created_at', 'updated_by')
    search_fields = ('title', 'content', 'excerpt')
    readonly_fields = (
        'post',
        'revision_number',
        'title',
        'content',
        'excerpt',
        'updated_by',
        'created_at',
        'changes',
        'content_diff'
    )

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"
    post_link.allow_tags = True

    def content_diff(self, obj):
        if not obj.previous_revision:
            return "No previous revision to compare with"
        return format_html("<pre>{}</pre>", "Content differences would appear here")
    content_diff.short_description = "Changes from previous version"
    content_diff.allow_tags = True

    def has_add_permission(self, request):
        return False