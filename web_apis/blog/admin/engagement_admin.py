# blog/admin/engagement_admin.py
# blog/admin/engagement_admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from web_apis.blog.models import Comment, CommentReaction, Like, PostReaction, Favorite

class CommentReactionInline(admin.TabularInline):
    model = CommentReaction
    extra = 0
    readonly_fields = ('user', 'reaction', 'created_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'truncated_content',
        'post_link',
        'user_display',
        'is_approved',
        'is_spam',
        'created_at',
        'ip_address'
    )
    list_filter = (
        'is_approved',
        'is_spam',
        'created_at',
        'post'
    )
    search_fields = (
        'content',
        'author_name',
        'guest_email',
        'user__email'
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'display_name',
        'author_email',
        'user_initials_display',  # Changed from user_initials
        'ip_address',
        'user_agent',
        'referrer',
        'is_reply'
    )
    raw_id_fields = ('user', 'post', 'parent')
    inlines = (CommentReactionInline,)
    actions = ['approve_comments', 'mark_as_spam']
    fieldsets = (
        (None, {
            'fields': (
                'post',
                'parent',
                'content'
            )
        }),
        ('Author', {
            'fields': (
                'user',
                'author_name',
                'guest_name',
                'guest_email',
                'display_name',
                'author_email',
                'user_initials_display'  # Changed here
            )
        }),
        ('Moderation', {
            'fields': (
                'is_approved',
                'is_spam'
            )
        }),
        ('Technical', {
            'classes': ('collapse',),
            'fields': (
                'ip_address',
                'user_agent',
                'referrer'
            )
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at'
            )
        })
    )

    def user_initials_display(self, obj):  # Added this method
        if obj.user:
            return ''.join([name[0] for name in obj.user.get_full_name().split()[:2]])
        elif obj.author_name:
            return obj.author_name[:2]
        return "--"
    user_initials_display.short_description = "Initials"

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"
    post_link.allow_tags = True

    def user_display(self, obj):
        if obj.user:
            url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return f"{obj.author_name} (guest)"
    user_display.short_description = "Author"
    user_display.allow_tags = True

    def truncated_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    truncated_content.short_description = "Content"

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True, is_approved=False)
    mark_as_spam.short_description = "Mark selected as spam"

# ... rest of your admin classes remain the same ...

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = (
        'comment_link',
        'user_link',
        'reaction_display',
        'created_at'
    )
    list_filter = ('reaction', 'created_at')
    search_fields = (
        'comment__content',
        'user__email'
    )
    readonly_fields = (
        'comment',
        'user',
        'created_at',
        'reaction_display'
    )

    def comment_link(self, obj):
        url = reverse('admin:blog_comment_change', args=[obj.comment.id])
        return format_html('<a href="{}">{}...</a>', url, obj.comment.content[:30])
    comment_link.short_description = "Comment"

    def user_link(self, obj):
        url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = "User"

    def reaction_display(self, obj):
        return obj.get_reaction_display()
    reaction_display.short_description = "Reaction"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'user_link',
        'created_at'
    )
    list_filter = ('created_at',)
    search_fields = (
        'post__title',
        'user__email'
    )
    readonly_fields = (
        'post',
        'user',
        'created_at'
    )
    raw_id_fields = ('post', 'user')

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"

    def user_link(self, obj):
        url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = "User"

@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'user_link',
        'reaction_display',
        'created_at'
    )
    list_filter = ('reaction', 'created_at')
    search_fields = (
        'post__title',
        'user__email'
    )
    readonly_fields = (
        'post',
        'user',
        'created_at',
        'reaction_display'
    )
    raw_id_fields = ('post', 'user')

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"

    def user_link(self, obj):
        url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = "User"

    def reaction_display(self, obj):
        return obj.get_reaction_display()
    reaction_display.short_description = "Reaction"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'post_link',
        'user_link',
        'created_at',
        'notes_preview'
    )
    list_filter = ('created_at',)
    search_fields = (
        'post__title',
        'user__email',
        'notes'
    )
    readonly_fields = (
        'post',
        'user',
        'created_at'
    )
    raw_id_fields = ('post', 'user')

    def post_link(self, obj):
        url = reverse('admin:blog_blogpost_change', args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post.title)
    post_link.short_description = "Post"

    def user_link(self, obj):
        url = reverse('admin:user_account_customuser_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = "User"

    def notes_preview(self, obj):
        return obj.notes[:30] + ("..." if len(obj.notes) > 30 else "")
    notes_preview.short_description = "Notes"