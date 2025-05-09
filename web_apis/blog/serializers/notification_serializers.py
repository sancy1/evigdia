
# blog/serializers/notification_serializers.py

from rest_framework import serializers
from blog.models.notification_models import Notification, AdminNotification
from blog_serializers import BlogPostMinimalSerializer
from user_account.serializers import UserMinimalSerializer

class NotificationSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    related_post = BlogPostMinimalSerializer(read_only=True)
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'notification_type',
            'notification_type_display',
            'message',
            'is_read',
            'target_url',
            'related_post',
            'created_at'
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add human-readable time difference
        data['time_since'] = instance.created_at.timesince()
        return data


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']
    
    def update(self, instance, validated_data):
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance


class AdminNotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = AdminNotification
        fields = [
            'id',
            'notification_type',
            'notification_type_display',
            'title',
            'message',
            'related_object_id',
            'related_content_type',
            'is_read',
            'created_at',
            'metadata'
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add human-readable time difference
        data['time_since'] = instance.created_at.timesince()
        return data


class AdminNotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminNotification
        fields = ['is_read']
    
    def update(self, instance, validated_data):
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance


# Dashboard serializers
class NotificationSummarySerializer(serializers.Serializer):
    notification_type = serializers.CharField()
    count = serializers.IntegerField()
    last_instance = serializers.DateTimeField()


class AdminNotificationSummarySerializer(serializers.Serializer):
    notification_type = serializers.CharField()
    count = serializers.IntegerField()
    last_instance = serializers.DateTimeField()


# Minimal serializers for lists
class NotificationMinimalSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'notification_type_display',
            'message',
            'is_read',
            'created_at'
        ]
        read_only_fields = fields


class AdminNotificationMinimalSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    
    class Meta:
        model = AdminNotification
        fields = [
            'id',
            'notification_type',
            'notification_type_display',
            'title',
            'is_read',
            'created_at'
        ]
        read_only_fields = fields