
# blog/serializers/syndication_serializers.py

from rest_framework import serializers
from blog.models.syndication_models import ContentSyndication
from blog.serializers.blog_serializers import BlogPostMinimalSerializer

class ContentSyndicationSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    published_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', 
        allow_null=True
    )
    platform_details = serializers.SerializerMethodField()
    
    class Meta:
        model = ContentSyndication
        fields = [
            'id',
            'post',
            'platform_name',
            'url',
            'published_at',
            'is_canonical',
            'metadata',
            'platform_details'
        ]
        read_only_fields = [
            'id',
            'post',
            'published_at'
        ]
    
    def get_platform_details(self, obj):
        return {
            'name': obj.platform_name,
            'url': obj.url,
            'is_canonical': obj.is_canonical
        }

class ContentSyndicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSyndication
        fields = [
            'post',
            'platform_name',
            'url',
            'published_at',
            'is_canonical',
            'metadata'
        ]
        extra_kwargs = {
            'post': {'required': True},
            'platform_name': {'required': True},
            'url': {'required': True}
        }
    
    def validate(self, data):
        # Ensure only one canonical version per platform
        if data.get('is_canonical', False):
            existing_canonical = ContentSyndication.objects.filter(
                post=data['post'],
                platform_name=data['platform_name'],
                is_canonical=True
            ).exists()
            
            if existing_canonical:
                raise serializers.ValidationError(
                    f"A canonical syndication already exists for this post on {data['platform_name']}"
                )
        return data

class ContentSyndicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSyndication
        fields = [
            'url',
            'published_at',
            'is_canonical',
            'metadata'
        ]
    
    def validate(self, data):
        if 'is_canonical' in data and data['is_canonical']:
            existing_canonical = ContentSyndication.objects.filter(
                post=self.instance.post,
                platform_name=self.instance.platform_name,
                is_canonical=True
            ).exclude(id=self.instance.id).exists()
            
            if existing_canonical:
                raise serializers.ValidationError(
                    f"A canonical syndication already exists for this post on {self.instance.platform_name}"
                )
        return data

# Minimal serializers for lists
class ContentSyndicationMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSyndication
        fields = [
            'id',
            'platform_name',
            'url',
            'published_at',
            'is_canonical'
        ]
        read_only_fields = fields

# Dashboard/analytics serializers
class SyndicationStatsSerializer(serializers.Serializer):
    platform_name = serializers.CharField()
    count = serializers.IntegerField()
    last_syndication = serializers.DateTimeField()
    canonical_count = serializers.IntegerField()