
# blog/serializers/subscription_serializers.py

from rest_framework import serializers
from blog.models.subscription_models import Subscription
from user_account.serializers import UserMinimalSerializer
from django.utils import timezone

class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    status = serializers.SerializerMethodField()
    subscribed_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    unsubscribed_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S',
        allow_null=True
    )
    
    class Meta:
        model = Subscription
        fields = [
            'id',
            'email',
            'user',
            'is_active',
            'is_confirmed',
            'status',
            'subscribed_at',
            'unsubscribed_at',
            'ip_address',
            'preferences'
        ]
        read_only_fields = [
            'id',
            'user',
            'is_confirmed',
            'subscribed_at',
            'unsubscribed_at',
            'ip_address'
        ]
    
    def get_status(self, obj):
        if not obj.is_active:
            return "unsubscribed"
        return "confirmed" if obj.is_confirmed else "pending"

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['email', 'preferences']
        extra_kwargs = {
            'email': {'required': True}
        }
    
    def validate_email(self, value):
        # Add any custom email validation here
        return value.lower()  # Store emails in lowercase

class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['is_active', 'preferences']
    
    def update(self, instance, validated_data):
        # Handle unsubscription timestamp
        if 'is_active' in validated_data and not validated_data['is_active']:
            if instance.is_active:  # Only set if changing from active to inactive
                instance.unsubscribed_at = timezone.now()
        return super().update(instance, validated_data)

class SubscriptionConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        # Add validation to check token matches email
        return data

# Minimal serializers for lists
class SubscriptionMinimalSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscription
        fields = [
            'id',
            'email',
            'status',
            'subscribed_at'
        ]
        read_only_fields = fields
    
    def get_status(self, obj):
        if not obj.is_active:
            return "unsubscribed"
        return "confirmed" if obj.is_confirmed else "pending"

# Dashboard/analytics serializers
class SubscriptionStatsSerializer(serializers.Serializer):
    total_subscribers = serializers.IntegerField()
    active_subscribers = serializers.IntegerField()
    pending_confirmation = serializers.IntegerField()
    new_this_month = serializers.IntegerField()
    unsubscribed_this_month = serializers.IntegerField()