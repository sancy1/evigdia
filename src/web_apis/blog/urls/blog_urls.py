
# blog/urls/blog_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from web_apis.blog.views.blog_views import (
    CategoryViewSet,
    TagViewSet,
    BlogPostViewSet,
    BlogPostRevisionViewSet
)

# Main router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'posts', BlogPostViewSet, basename='post')

# Nested router for revisions
posts_router = DefaultRouter()
posts_router.register(r'revisions', BlogPostRevisionViewSet, basename='post-revision')

urlpatterns = [
    # Main API endpoints
    path('', include(router.urls)),

    # Post-specific nested routes - ADJUSTED TO USE SLUG
    path('posts/<slug:slug>/', include(posts_router.urls)),
    # Custom actions - ADJUSTED TO USE SLUG
    path('posts/<slug:slug>/publish/',
        BlogPostViewSet.as_view({'post': 'publish'}),
        name='post-publish'),
    path('posts/<slug:slug>/feature/',
        BlogPostViewSet.as_view({'post': 'feature'}),
        name='post-feature'),
    path('posts/<slug:slug>/restore-revision/',
        BlogPostViewSet.as_view({'post': 'restore_revision'}),
        name='post-restore-revision'),
    path('posts/<slug:slug>/feature/',  # Added endpoint for the 'feature' action
        BlogPostViewSet.as_view({'post': 'feature'}),
        name='post-feature'),
    path('posts/<slug:slug>/pin/',  # Added endpoint for the 'pin' action
        BlogPostViewSet.as_view({'post': 'pin'}),
        name='post-pin'),
    
    path('posts/<slug:slug>/revisions/',  # Endpoint to list all revisions for a post
        BlogPostViewSet.as_view({'get': 'revisions'}),
        name='post-revisions'),

    path('categories/<uuid:id>/restore/',
        CategoryViewSet.as_view({'post': 'restore'}),
        name='category-restore'),
    path('categories/<uuid:id>/hard_delete/',  # URL for the chosen hard delete option
        CategoryViewSet.as_view({'delete': 'hard_delete'}),
        name='category-hard-delete'),

    path('tags/<uuid:id>/restore/',
        TagViewSet.as_view({'post': 'restore'}),
        name='tag-restore'),
    path('tags/<uuid:id>/hard_delete/',  # New URL for hard delete action for tags
        TagViewSet.as_view({'delete': 'hard_delete'}),
        name='tag-hard-delete'),
    
    path('posts/<slug:slug>/toggle-status/',
        BlogPostViewSet.as_view({'post': 'toggle_status'}),
        name='post-toggle-status'),
    path('posts/<slug:slug>/publish/',
        BlogPostViewSet.as_view({'post': 'publish'}),
        name='post-publish'),
    path('posts/<slug:slug>/archive/',
        BlogPostViewSet.as_view({'post': 'archive'}),
        name='post-archive'),
    path('posts/<slug:slug>/schedule/',
        BlogPostViewSet.as_view({'post': 'schedule'}),
        name='post-schedule'),
]