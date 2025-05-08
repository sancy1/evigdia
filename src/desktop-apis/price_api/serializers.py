
from rest_framework import serializers
from .models import SubscriptionPrice

class SubscriptionPriceSerializer(serializers.ModelSerializer):
    plan_type_display = serializers.CharField(source='get_plan_type_display', read_only=True)

    class Meta:
        model = SubscriptionPrice
        fields = ['plan_type', 'plan_type_display', 'price_usd', 'description', 'last_updated', 'is_active']
        read_only_fields = ['last_updated']
        
        