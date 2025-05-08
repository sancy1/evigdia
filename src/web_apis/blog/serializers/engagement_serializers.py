


# blog/serializers/engagement_serializers.py

from rest_framework import serializers
from blog.models import (
    Comment,
    CommentReaction,
    Like,
    PostReaction,
    Favorite
)
from blog_serializers import BlogPostMinimalSerializer
from user_account.serializers import UserMinimalSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    post = BlogPostMinimalSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)
    replies = serializers.SerializerMethodField()
    is_reply = serializers.BooleanField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    author_email = serializers.EmailField(read_only=True)
    user_initials = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'parent',
            'replies',
            'author_name',
            'author_email',
            'guest_name',
            'guest_email',
            'content',
            'is_approved',
            'is_spam',
            'is_reply',
            'display_name',
            'user_initials',  # Add this line
            'ip_address',
            'user_agent',
            'referrer',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'is_reply',
            'display_name',
            'author_email',
            'user_initials'  # Add this line
        ]
    
    def get_replies(self, obj):
        if hasattr(obj, 'replies_count'):
            return obj.replies_count
        return obj.replies.count()
    
    def get_user_initials(self, obj):
        if obj.user:
            return obj.user.get_initials() if hasattr(obj.user, 'get_initials') else ''
        return ''

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'post',
            'parent',
            'author_name',
            'guest_name',
            'guest_email',
            'content'
        ]
        extra_kwargs = {
            'content': {'required': True, 'allow_blank': False},
            'post': {'required': True}
        }
    
    def validate(self, data):
        request = self.context.get('request')
        if request and not request.user.is_authenticated:
            if not data.get('author_name'):
                raise serializers.ValidationError("Name is required for guest comments")
            if not data.get('guest_email'):
                raise serializers.ValidationError("Email is required for guest comments")
        return data

class CommentReactionSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    reaction_display = serializers.CharField(source='get_reaction_display', read_only=True)
    user_initials = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = CommentReaction
        fields = [
            'id',
            'user',
            'comment',
            'reaction',
            'reaction_display',
            'user_initials',  # Add this line
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'reaction_display', 'user_initials']
    
    def get_user_initials(self, obj):
        return obj.user.get_initials() if hasattr(obj.user, 'get_initials') else ''

class LikeSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    post = BlogPostMinimalSerializer(read_only=True)
    user_initials = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'post',
            'user_initials',  # Add this line
            'created_at'
        ]
        read_only_fields = fields
    
    def get_user_initials(self, obj):
        return obj.user.get_initials() if hasattr(obj.user, 'get_initials') else ''

class PostReactionSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    post = BlogPostMinimalSerializer(read_only=True)
    reaction_display = serializers.CharField(source='get_reaction_display', read_only=True)
    user_initials = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = PostReaction
        fields = [
            'id',
            'user',
            'post',
            'reaction',
            'reaction_display',
            'user_initials',  # Add this line
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'reaction_display', 'user_initials']
    
    def get_user_initials(self, obj):
        return obj.user.get_initials() if hasattr(obj.user, 'get_initials') else ''

class FavoriteSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    post = BlogPostMinimalSerializer(read_only=True)
    user_initials = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = Favorite
        fields = [
            'id',
            'user',
            'post',
            'notes',
            'user_initials',  # Add this line
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'user_initials']
    
    def get_user_initials(self, obj):
        return obj.user.get_initials() if hasattr(obj.user, 'get_initials') else ''

# Nested serializers for related fields
class CommentMinimalSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    display_name = serializers.CharField(read_only=True)
    user_initials = serializers.SerializerMethodField()  # Add this line
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'display_name',
            'user_initials',  # Add this line
            'content',
            'created_at'
        ]
        read_only_fields = fields
    
    def get_user_initials(self, obj):
        return obj.user.get_initials() if hasattr(obj.user, 'get_initials') else ''

# [Rest of your minimal serializers remain the same...]

class CommentReactionMinimalSerializer(serializers.ModelSerializer):
    reaction_display = serializers.CharField(source='get_reaction_display', read_only=True)
    
    class Meta:
        model = CommentReaction
        fields = [
            'id',
            'reaction',
            'reaction_display',
            'created_at'
        ]
        read_only_fields = fields

class PostReactionMinimalSerializer(serializers.ModelSerializer):
    reaction_display = serializers.CharField(source='get_reaction_display', read_only=True)
    
    class Meta:
        model = PostReaction
        fields = [
            'id',
            'reaction',
            'reaction_display',
            'created_at'
        ]
        read_only_fields = fields

class FavoriteMinimalSerializer(serializers.ModelSerializer):
    post = BlogPostMinimalSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = [
            'id',
            'post',
            'created_at'
        ]
        read_only_fields = fields