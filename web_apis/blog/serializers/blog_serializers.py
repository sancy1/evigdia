# blog/serializers/blog_serializers.py

from rest_framework import serializers
from web_apis.blog.models import Category, Tag, BlogPost, BlogPostRevision
from user_account.serializers import UserSerializer  # Assuming you have a UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'meta_title',
            'meta_description',
            'is_active',
            'created_at',
            'updated_at',
            'absolute_url'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'absolute_url']

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class TagSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'is_active',
            'created_at',
            'updated_at',
            'absolute_url'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'absolute_url']

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class BlogPostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'author',
            'categories',
            'tags',
            'status',
            'status_display',
            'is_featured',
            'is_pinned',
            'featured_image',
            'featured_image_alt',
            'reading_time',
            'view_count',
            'comment_count',
            'like_count',
            'published_at',
            'created_at',
            'absolute_url'
        ]
        read_only_fields = fields

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class BlogPostDetailSerializer(BlogPostListSerializer):
    related_posts = BlogPostListSerializer(many=True, read_only=True)
    is_public = serializers.BooleanField(read_only=True)
    is_scheduled = serializers.BooleanField(read_only=True)

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            'content',
            'rendered_content',
            'related_posts',
            'allow_comments',
            'embedded_media',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'canonical_url',
            'word_count',
            'code_snippets',
            'is_public',
            'is_scheduled',
            'scheduled_at',
            'updated_at'
        ]
        read_only_fields = fields


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'excerpt',
            'content',
            'categories',
            'tags',
            'related_posts',
            'status',
            'is_featured',
            'is_pinned',
            'allow_comments',
            'featured_image',
            'featured_image_alt',
            'embedded_media',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'canonical_url',
            'scheduled_at'
        ]

    def validate(self, data):
        if data.get('status') == BlogPost.PostStatus.PUBLISHED and not self.instance:
            if not data.get('content') or len(data['content'].split()) < 500:
                raise serializers.ValidationError(
                    "Published posts must have at least 500 words"
                )
        return data

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        tags = validated_data.pop('tags', [])
        related_posts = validated_data.pop('related_posts', [])

        post = BlogPost.objects.create(
            **validated_data  # Removed author=self.context['request'].user
        )

        post.categories.set(categories)
        post.tags.set(tags)
        post.related_posts.set(related_posts)

        return post

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        tags = validated_data.pop('tags', None)
        related_posts = validated_data.pop('related_posts', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if categories is not None:
            instance.categories.set(categories)
        if tags is not None:
            instance.tags.set(tags)
        if related_posts is not None:
            instance.related_posts.set(related_posts)

        instance.save()
        return instance


class BlogPostRevisionSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    revision_summary = serializers.SerializerMethodField()

    class Meta:
        model = BlogPostRevision
        fields = [
            'id',
            'post',
            'revision_number',
            'title',
            'content',
            'excerpt',
            'updated_by',
            'created_at',
            'revision_notes',
            'changes',
            'revision_summary'
        ]
        read_only_fields = fields

    def get_revision_summary(self, obj):
        return str(obj)


# Mini serializers for nested representations
class CategoryMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TagMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BlogPostMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'published_at']