
# blog/serializers/sharing_serializers.py

from rest_framework import serializers
from blog.models.sharing_models import SocialPlatform, ShareTracking, ShareableLink
from blog.serializers.blog_serializers import BlogPostMinimalSerializer
from user_account.serializers import UserMinimalSerializer
from django.utils import timezone

class SocialPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPlatform
        fields = [
            'id',
            'name',
            'base_share_url',
            'icon_class',
            'is_active',
            'order'
        ]
        read_only_fields = ['id']

class ShareTrackingSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    platform = SocialPlatformSerializer(read_only=True)
    user = UserMinimalSerializer(read_only=True)
    share_method_display = serializers.CharField(
        source='get_share_method_display',
        read_only=True
    )
    shared_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    share_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ShareTracking
        fields = [
            'id',
            'post',
            'platform',
            'user',
            'share_method',
            'share_method_display',
            'ip_address',
            'user_agent',
            'referrer',
            'shared_at',
            'clickback_count',
            'metadata',
            'share_details'
        ]
        read_only_fields = fields
    
    def get_share_details(self, obj):
        details = {
            'platform': obj.platform.name if obj.platform else 'Direct',
            'shared_by': obj.user.email if obj.user else 'Anonymous',
            'content': obj.post.title
        }
        details.update(obj.metadata)
        return details

class ShareableLinkSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    creator = UserMinimalSerializer(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    is_expired = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    expiration = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        allow_null=True
    )
    
    class Meta:
        model = ShareableLink
        fields = [
            'id',
            'post',
            'creator',
            'token',
            'absolute_url',
            'expiration',
            'max_uses',
            'use_count',
            'created_at',
            'notes',
            'is_active',
            'is_expired'
        ]
        read_only_fields = [
            'id',
            'token',
            'absolute_url',
            'use_count',
            'created_at',
            'is_expired'
        ]
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

class ShareableLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareableLink
        fields = [
            'post',
            'expiration',
            'max_uses',
            'notes',
            'is_active'
        ]
        extra_kwargs = {
            'post': {'required': True}
        }
    
    def validate(self, data):
        if data.get('expiration') and data['expiration'] < timezone.now():
            raise serializers.ValidationError(
                "Expiration date must be in the future"
            )
        if data.get('max_uses') is not None and data['max_uses'] <= 0:
            raise serializers.ValidationError(
                "Max uses must be a positive number"
            )
        return data

# Dashboard/Summary Serializers
class ShareAnalyticsSerializer(serializers.Serializer):
    post = BlogPostMinimalSerializer()
    total_shares = serializers.IntegerField()
    unique_sharers = serializers.IntegerField()
    top_platform = serializers.CharField()
    clickback_rate = serializers.FloatField()

class PlatformShareStatsSerializer(serializers.Serializer):
    platform = SocialPlatformSerializer()
    share_count = serializers.IntegerField()
    clickback_count = serializers.IntegerField()
    clickback_rate = serializers.FloatField()

# Minimal serializers for nested representations
class ShareTrackingMinimalSerializer(serializers.ModelSerializer):
    platform = SocialPlatformSerializer(read_only=True)
    
    class Meta:
        model = ShareTracking
        fields = [
            'id',
            'platform',
            'share_method',
            'shared_at',
            'clickback_count'
        ]
        read_only_fields = fields

class ShareableLinkMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareableLink
        fields = [
            'id',
            'token',
            'is_expired',
            'use_count',
            'created_at'
        ]
        read_only_fields = fields