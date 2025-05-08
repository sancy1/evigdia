
# blog/views/blog_views.py

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from django.core.exceptions import PermissionDenied
from web_apis.blog.models.blog_models import Category, Tag, BlogPost, BlogPostRevision
from web_apis.blog.serializers.blog_serializers import (
    CategorySerializer,
    TagSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateUpdateSerializer,
    BlogPostRevisionSerializer
)
from web_apis.blog.services.blog_service import BlogPostService
from web_apis.blog.validators.blog_validators import BlogPostValidator
from user_account.permissions import IsStaffOrReadOnly, IsAuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination



# Category View -------------------------------------------------------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'status': f'Category "{instance.name}" has been deactivated successfully.'},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        """Soft delete by marking as inactive"""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['post'])
    def restore(self, request, id=None):
        """Restore inactive category (admin only)"""
        category = self.get_object()
        if category.is_active:
            return Response({'status': 'Category is already active'},
                            status=status.HTTP_400_BAD_REQUEST)
        category.is_active = True
        category.save()
        return Response({'status': 'Category restored'})



# Tag View -------------------------------------------------------------------------
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'status': f'Tag "{instance.name}" has been deactivated successfully.'},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self, instance):
        """Soft delete by marking as inactive"""
        instance.is_active = False
        instance.save()

 
    @action(detail=True, methods=['post'])
    def restore(self, request, id=None):
        """Restore inactive tag (admin only)"""
        tag = self.get_object()
        if tag.is_active:
            return Response({'status': 'Tag is already active'},
                            status=status.HTTP_400_BAD_REQUEST)
        tag.is_active = True
        tag.save()
        return Response({'status': 'Tag restored'})

    @action(detail=True, methods=['delete'], permission_classes=[IsAdminUser])
    def hard_delete(self, request, id=None):
        """Permanently delete a tag (superuser only)"""
        tag = self.get_object()
        associated_posts_count = tag.blog_posts.count()
        if associated_posts_count > 0:
            return Response(
                {'error': f'Cannot permanently delete tag with {associated_posts_count} associated posts.'},
                status=status.HTTP_409_CONFLICT  # Conflict status
            )
        tag.delete()
        return Response({'status': f'Tag with ID {id} permanently deleted.'}, status=status.HTTP_204_NO_CONTENT)
    


# Blog Post View -------------------------------------------------------------------------
class BlogPostViewSet(viewsets.ModelViewSet, PageNumberPagination):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostListSerializer
    lookup_field = 'slug'
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    page_size = 12

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BlogPostCreateUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-published_at', '-created_at')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

        # Apply filters
        params = self.request.query_params
        status_filter = params.get('status')
        category = params.get('category')
        tag = params.get('tag')
        featured = params.get('featured')
        search = params.get('search')
        author = params.get('author')

        # Base filtering
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status=BlogPost.PostStatus.PUBLISHED) &
                Q(published_at__lte=timezone.now())
            )
        elif status_filter:
            queryset = queryset.filter(status=status_filter)

        if category:
            queryset = queryset.filter(categories__id=category)

        if tag:
            queryset = queryset.filter(tags__id=tag)

        if featured:
            queryset = queryset.filter(is_featured=True)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )

        if author:
            queryset = queryset.filter(author__id=author)

        # Optimize queries
        queryset = queryset.select_related('author')
        queryset = queryset.prefetch_related('categories', 'tags', 'related_posts')
        queryset = queryset.annotate(
            num_comments=Count('comments', distinct=True), # Changed the annotation name
            num_likes=Count('likes', distinct=True)        # Changed the annotation name
        )

        return queryset.order_by('-published_at', '-created_at')

    def perform_create(self, serializer):
        # BlogPostValidator.validate_post_create(self.request.data)
        serializer.save(author=self.request.user)  # Keep setting author here
        # BlogPostService.handle_post_creation(post, serializer.validated_data)

    def perform_update(self, serializer):
        # BlogPostValidator.validate_post_update(self.request.data)
        serializer.save()
        # BlogPostService.handle_post_update(serializer.instance, serializer.validated_data)

    def perform_destroy(self, instance):
        # BlogPostService.archive_post(instance)
        instance.status = BlogPost.PostStatus.ARCHIVED
        instance.save()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()  # This line performs the actual deletion
            return Response(
            {'status': 'success', 'message': 'Post was successfully archived'},
            status=status.HTTP_200_OK
        )
        except Exception as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        """Publish a draft post"""
        post = self.get_object()
        if post.status != BlogPost.PostStatus.DRAFT:
            return Response(
                {'error': 'Only draft posts can be published'},
                status=status.HTTP_400_BAD_REQUEST
            )
        post.published_at = timezone.now()
        post.status = BlogPost.PostStatus.PUBLISHED
        post.save()
        return Response({'status': 'Post published'})

    @action(detail=True, methods=['post'])
    def feature(self, request, slug=None):
        """Toggle featured status"""
        post = self.get_object()
        post.is_featured = not post.is_featured
        post.save()
        return Response({'status': 'Featured' if post.is_featured else 'Unfeatured'})

    @action(detail=True, methods=['get'])
    def revisions(self, request, slug=None):
        """Get all revisions for a post"""
        post = self.get_object()
        revisions = post.revisions.all().order_by('-revision_number')
        serializer = BlogPostRevisionSerializer(revisions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore_revision(self, request, slug=None, revision_number=None):
        """Restore a specific revision"""
        post = self.get_object()
        revision = get_object_or_404(
            post.revisions,
            revision_number=request.data.get('revision_number')
        )
        post.title = revision.title
        post.content = revision.content
        post.excerpt = revision.excerpt
        post.save()
        return Response({'status': 'Revision restored'})
    
    
    @action(detail=True, methods=['post'])
    def pin(self, request, slug=None):
        """Toggle pinned status"""
        post = self.get_object()
        post.is_pinned = not post.is_pinned
        post.save()
        return Response({'status': 'Pinned' if post.is_pinned else 'Unpinned'})


    @action(detail=True, methods=['post'])
    def toggle_status(self, request, slug=None):
        """Toggle the status of a blog post between 'draft' and 'published'."""
        post = self.get_object()
        if post.status == BlogPost.PostStatus.DRAFT:
            post.status = BlogPost.PostStatus.PUBLISHED
            post.published_at = timezone.now() # Or handle scheduled_at if needed
            message = f"Post '{post.title}' has been published."
        elif post.status == BlogPost.PostStatus.PUBLISHED:
            post.status = BlogPost.PostStatus.DRAFT
            post.published_at = None
            message = f"Post '{post.title}' has been moved to draft."
        else:
            return Response(
                {'error': f"Cannot toggle status from '{post.get_status_display()}'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        post.save()
        return Response({'status': 'success', 'message': message})

    # You can create separate actions for more specific status changes if needed
    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        """Specifically publish a draft post."""
        post = self.get_object()
        if post.status != BlogPost.PostStatus.DRAFT:
            return Response(
                {'error': 'Only draft posts can be published using this action.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        post.status = BlogPost.PostStatus.PUBLISHED
        post.published_at = timezone.now()
        post.save()
        return Response({'status': 'success', 'message': f"Post '{post.title}' has been published."})

    @action(detail=True, methods=['post'])
    def archive(self, request, slug=None):
        """Archive a blog post."""
        post = self.get_object()
        post.status = BlogPost.PostStatus.ARCHIVED
        post.save()
        return Response({'status': 'success', 'message': f"Post '{post.title}' has been archived."})

    @action(detail=True, methods=['post'])
    def schedule(self, request, slug=None):
        """Schedule a blog post."""
        post = self.get_object()
        scheduled_at = request.data.get('scheduled_at')
        if not scheduled_at:
            return Response(
                {'error': 'Please provide a "scheduled_at" timestamp.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            post.scheduled_at = scheduled_at
            post.status = BlogPost.PostStatus.SCHEDULED
            post.save()
            return Response({'status': 'success', 'message': f"Post '{post.title}' has been scheduled for {scheduled_at}."})
        except ValueError:
            return Response(
                {'error': 'Invalid "scheduled_at" timestamp format.'},
                status=status.HTTP_400_BAD_REQUEST
            )



# Blog Post Revision View -------------------------------------------------------------------------
class BlogPostRevisionViewSet(mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPostRevision.objects.all()
    serializer_class = BlogPostRevisionSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return BlogPostRevision.objects.filter(
            post__id=post_id
        ).order_by('-revision_number')