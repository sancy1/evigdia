
from rest_framework import serializers
from .models import AppManager, GlobalAppControl

class AppManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppManager
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class GlobalAppControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalAppControl
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AppStatusSerializer(serializers.Serializer):
    api_key = serializers.CharField(required=True)
    app_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of app types to check status for"
    )