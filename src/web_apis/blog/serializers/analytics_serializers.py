
# blog/serializers/analytics_serializers.py

from rest_framework import serializers
from blog.models.analytics_models import (
    PostView,
    ReadHistory,
    SearchQuery,
    ClickEvent,
    AdminActivityLog
)
from blog.serializers.blog_serializers import BlogPostMinimalSerializer
from user_account.serializers import UserMinimalSerializer

class PostViewSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    user = UserMinimalSerializer(read_only=True)
    viewer_display = serializers.SerializerMethodField()
    viewed_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = PostView
        fields = [
            'id',
            'post',
            'user',
            'ip_address',
            'user_agent',
            'referrer',
            'viewed_at',
            'time_spent',
            'viewer_display'
        ]
        read_only_fields = fields
    
    def get_viewer_display(self, obj):
        if obj.user:
            return f"{obj.user.email} ({obj.ip_address})"
        return f"Anonymous ({obj.ip_address})"


class ReadHistorySerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    user = UserMinimalSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    reading_status = serializers.SerializerMethodField()
    last_read_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = ReadHistory
        fields = [
            'id',
            'user',
            'post',
            'last_read_at',
            'read_count',
            'is_completed',
            'scroll_position',
            'progress_percentage',
            'reading_status'
        ]
        read_only_fields = fields
    
    def get_progress_percentage(self, obj):
        if obj.post.word_count > 0:
            return min(100, (obj.scroll_position / obj.post.word_count) * 100)
        return 0
    
    def get_reading_status(self, obj):
        if obj.is_completed:
            return "completed"
        elif obj.scroll_position > 0:
            return "in_progress"
        return "not_started"


class SearchQuerySerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    search_summary = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = SearchQuery
        fields = [
            'id',
            'query',
            'user',
            'ip_address',
            'results_count',
            'created_at',
            'search_summary'
        ]
        read_only_fields = fields
    
    def get_search_summary(self, obj):
        if obj.user:
            return f"{obj.user.email} searched for '{obj.query}'"
        return f"Anonymous user searched for '{obj.query}'"


class ClickEventSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    user = UserMinimalSerializer(read_only=True)
    click_details = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = ClickEvent
        fields = [
            'id',
            'post',
            'element_type',
            'element_id',
            'element_text',
            'url',
            'user',
            'ip_address',
            'created_at',
            'click_details'
        ]
        read_only_fields = fields
    
    def get_click_details(self, obj):
        details = {
            'element': f"{obj.element_type}: {obj.element_text or obj.element_id}",
            'action': f"Clicked on {obj.element_type} in {obj.post.title}"
        }
        if obj.url:
            details['destination'] = obj.url
        return details


class AdminActivityLogSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    post = BlogPostMinimalSerializer(read_only=True)
    activity_details = serializers.SerializerMethodField()
    activity_type_display = serializers.CharField(
        source='get_activity_type_display',
        read_only=True
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = AdminActivityLog
        fields = [
            'id',
            'activity_type',
            'activity_type_display',
            'user',
            'post',
            'ip_address',
            'metadata',
            'created_at',
            'is_processed',
            'activity_details'
        ]
        read_only_fields = fields
    
    def get_activity_details(self, obj):
        details = {
            'type': obj.get_activity_type_display(),
            'action': f"{obj.user.email if obj.user else 'System'} performed {obj.get_activity_type_display()}"
        }
        if obj.post:
            details['post'] = obj.post.title
        return details


# Dashboard/Summary Serializers
class PostAnalyticsSerializer(serializers.Serializer):
    post = BlogPostMinimalSerializer()
    total_views = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    average_time_spent = serializers.FloatField()
    completion_rate = serializers.FloatField()


class UserEngagementSerializer(serializers.Serializer):
    user = UserMinimalSerializer()
    total_views = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    total_shares = serializers.IntegerField()
    last_activity = serializers.DateTimeField()


class TrendAnalysisSerializer(serializers.Serializer):
    date = serializers.DateField()
    views = serializers.IntegerField()
    reads = serializers.IntegerField()
    shares = serializers.IntegerField()


# Lightweight Nested Serializers
class PostViewMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = ['id', 'viewed_at', 'time_spent', 'ip_address']


class ReadHistoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadHistory
        fields = ['id', 'last_read_at', 'is_completed', 'scroll_position']


class SearchQueryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = ['id', 'query', 'created_at', 'results_count']


class ClickEventMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickEvent
        fields = ['id', 'element_type', 'element_text', 'created_at']


class AdminActivityMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminActivityLog
        fields = ['id', 'activity_type', 'created_at', 'is_processed']