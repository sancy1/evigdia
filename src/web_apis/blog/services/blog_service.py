
# blog/services/blog_service.py

from django.utils import timezone
from django.db import transaction, models
from django.core.exceptions import ValidationError
from web_apis.blog.models.blog_models import BlogPost, BlogPostRevision

class BlogPostService:
    
    @classmethod
    @transaction.atomic
    def create_post(cls, author, validated_data):
        """
        Creates a new blog post with all related data
        """
        categories = validated_data.pop('categories', [])
        tags = validated_data.pop('tags', [])
        related_posts = validated_data.pop('related_posts', [])
        
        # Create post - removed rendered_content generation
        post = BlogPost.objects.create(
            author=author,
            **validated_data
        )
        
        # Set relationships
        post.categories.set(categories)
        post.tags.set(tags)
        post.related_posts.set(related_posts)
        
        # Create initial revision
        cls._create_initial_revision(post)
        
        return post

    @classmethod
    @transaction.atomic
    def handle_post_update(cls, post, validated_data):
        """
        Handles post update with revision tracking
        """
        # Create revision before updating
        cls._create_revision(post, "Content updated")
        
        # Handle status changes
        if 'status' in validated_data:
            cls._handle_status_change(post, validated_data['status'])
        
        # Update fields
        for attr, value in validated_data.items():
            setattr(post, attr, value)
        
        post.save()
        return post

    @classmethod
    def archive_post(cls, post):
        """
        Archives a post (soft delete)
        """
        post.status = BlogPost.PostStatus.ARCHIVED
        post.save()

    @classmethod
    def publish_post(cls, post):
        """
        Publishes a draft post
        """
        if post.status != BlogPost.PostStatus.PUBLISHED:
            post.status = BlogPost.PostStatus.PUBLISHED
            post.published_at = timezone.now()
            post.save()
            cls._create_revision(post, "Post published")

    @classmethod
    def restore_revision(cls, post, revision):
        """
        Restores a post to a specific revision
        """
        post.title = revision.title
        post.content = revision.content
        post.excerpt = revision.excerpt
        post.save()
        cls._create_revision(post, f"Restored to revision {revision.revision_number}")

    @classmethod
    def increment_view_count(cls, post):
        """
        Atomically increments view count
        """
        BlogPost.objects.filter(id=post.id).update(
            view_count=models.F('view_count') + 1
        )

    @classmethod
    def _create_initial_revision(cls, post):
        """
        Creates the first revision for a new post
        """
        BlogPostRevision.objects.create(
            post=post,
            revision_number=1,
            title=post.title,
            content=post.content,
            excerpt=post.excerpt,
            updated_by=post.author,
            changes="Initial version"
        )

    @classmethod
    def _create_revision(cls, post, changes):
        """
        Creates a new revision for a post
        """
        last_revision = post.revisions.order_by('-revision_number').first()
        revision_number = last_revision.revision_number + 1 if last_revision else 1
        
        BlogPostRevision.objects.create(
            post=post,
            revision_number=revision_number,
            title=post.title,
            content=post.content,
            excerpt=post.excerpt,
            updated_by=post.author,
            changes=changes
        )

    @classmethod
    def _handle_status_change(cls, post, new_status):
        """
        Handles special logic for status changes
        """
        if new_status == BlogPost.PostStatus.PUBLISHED and not post.published_at:
            post.published_at = timezone.now()
        elif new_status == BlogPost.PostStatus.SCHEDULED:
            if not post.scheduled_at:
                raise ValidationError("Scheduled posts must have a scheduled_at date")