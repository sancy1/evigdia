
# blog/models/blog_models.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# --------------------------
# CORE CONTENT MODELS
# --------------------------

# CATEGORY -----------------------------------------------------------------------------------------
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)  # For font-awesome or similar icons
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'id': self.id})



# TAG -----------------------------------------------------------------------------------------
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'id': self.id})



# BLOG-POST -----------------------------------------------------------------------------------------
class BlogPost(models.Model):
    class PostStatus(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
        SCHEDULED = 'scheduled', _('Scheduled')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        limit_choices_to={'is_staff': True}
    )

    # Core content
    title = models.CharField(max_length=255, validators=[MinLengthValidator(10)])
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.TextField(
        max_length=200,
        blank=True,
        help_text=_("Brief summary of the post")
    )
    content = models.TextField(
        validators=[MinLengthValidator(200)],
        help_text=_("Main content of the blog post")
    )
    rendered_content = models.TextField(
        blank=True,
        help_text=_("HTML rendered content for faster display")
    )

    # Categorization
    categories = models.ManyToManyField(
        Category,
        related_name='blog_posts',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='blog_posts',
        blank=True
    )
    related_posts = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        help_text=_("Manually selected related posts")
    )

    # Status & timing
    status = models.CharField(
        max_length=10,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT
    )
    is_featured = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Set future date/time for scheduled publishing")
    )

    # Media
    featured_image = models.ImageField(
        upload_to='blog/featured_images/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text=_("Featured image for the blog post")
    )
    featured_image_alt = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Alt text for the featured image")
    )
    embedded_media = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of embedded media (YouTube, Twitter, etc.)")
    )

    # SEO
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text=_("Title for SEO (max 70 chars)")
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text=_("Description for SEO (max 160 chars)")
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Comma-separated keywords for SEO")
    )
    canonical_url = models.URLField(
        blank=True,
        help_text=_("Canonical URL for SEO if this content appears elsewhere")
    )

    # Reading metrics
    reading_time = models.PositiveSmallIntegerField(
        default=0,
        help_text=_("Estimated reading time in minutes")
    )
    word_count = models.PositiveIntegerField(default=0)

    # Stats (denormalized for performance)
    view_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)

    # Code snippets (can be stored as JSON or as separate model)
    # code_snippets = models.JSONField(
    #     default=list,
    #     blank=True,
    #     help_text=_("List of code snippets with language and content")
    # )

    code_snippets_data = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of code snippets with language and content")
    )

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['author']),
            models.Index(fields=['is_featured']),
        ]
        # paginate_by = 10  # Default items per page
        # paginate_by_param = 'page_size'
        # max_paginate_by = 100

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.PostStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        # Calculate reading time and word count
        self.word_count = len(self.content.split())
        self.reading_time = max(1, round(self.word_count / 200))  # 200 wpm reading speed

        # Set meta fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def is_public(self):
        return (
            self.status == self.PostStatus.PUBLISHED and
            self.published_at is not None and
            self.published_at <= timezone.now()
        )

    @property
    def is_scheduled(self):
        return (
            self.status == self.PostStatus.SCHEDULED and
            self.scheduled_at and
            self.scheduled_at > timezone.now()
        )



# BLOG-POST REVISION -----------------------------------------------------------------------------------------
class BlogPostRevision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revision_notes = models.TextField(blank=True)
    changes = models.TextField(blank=True, help_text=_("Summary of changes in this revision"))

    class Meta:
        verbose_name = _("Post Revision")
        verbose_name_plural = _("Post Revisions")
        ordering = ['-revision_number']
        unique_together = ('post', 'revision_number')

    def __str__(self):
        return f"Revision {self.revision_number} of {self.post.title}"