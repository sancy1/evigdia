

# blog/serializers/content_serializers.py

from rest_framework import serializers
from blog.models.content_models import MediaAttachment, CodeSnippet
from blog.serializers.blog_serializers import BlogPostMinimalSerializer
from user_account.serializers import UserMinimalSerializer

class MediaAttachmentSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    created_by = UserMinimalSerializer(read_only=True)
    media_type_display = serializers.CharField(
        source='get_media_type_display',
        read_only=True
    )
    file_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = MediaAttachment
        fields = [
            'id',
            'post',
            'upload',
            'file_url',
            'url',
            'media_type',
            'media_type_display',
            'caption',
            'alt_text',
            'created_at',
            'created_by'
        ]
        read_only_fields = [
            'id',
            'media_type_display',
            'file_url',
            'created_at',
            'created_by'
        ]
    
    def get_file_url(self, obj):
        if obj.upload:
            return obj.upload.url
        return None

class MediaAttachmentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAttachment
        fields = [
            'post',
            'upload',
            'url',
            'media_type',
            'caption',
            'alt_text'
        ]
        extra_kwargs = {
            'upload': {'required': False},
            'url': {'required': False}
        }
    
    def validate(self, data):
        if not data.get('upload') and not data.get('url'):
            raise serializers.ValidationError(
                "Either upload or URL must be provided"
            )
        if data.get('upload') and data.get('url'):
            raise serializers.ValidationError(
                "Cannot provide both upload and URL"
            )
        return data

class CodeSnippetSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = CodeSnippet
        fields = [
            'id',
            'post',
            'language',
            'code',
            'caption',
            'line_numbers',
            'highlighted_lines',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'created_at'
        ]

class CodeSnippetCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = [
            'post',
            'language',
            'code',
            'caption',
            'line_numbers',
            'highlighted_lines'
        ]
        extra_kwargs = {
            'post': {'required': True},
            'language': {'required': True},
            'code': {'required': True}
        }
    
    def validate_highlighted_lines(self, value):
        if value:
            try:
                # Validate highlighted lines format (e.g., "1-5,7,9-12")
                parts = value.split(',')
                for part in parts:
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        if start > end:
                            raise ValueError
                    else:
                        int(part)
            except ValueError:
                raise serializers.ValidationError(
                    "Highlighted lines must be in format like '1-5,7,9-12'"
                )
        return value

# Minimal serializers for nested representations
class MediaAttachmentMinimalSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaAttachment
        fields = [
            'id',
            'media_type',
            'file_url',
            'url',
            'caption'
        ]
        read_only_fields = fields
    
    def get_file_url(self, obj):
        if obj.upload:
            return obj.upload.url
        return None

class CodeSnippetMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet
        fields = [
            'id',
            'language',
            'caption'
        ]
        read_only_fields = fields