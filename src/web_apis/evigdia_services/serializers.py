

# web_apis/evigdia_services/serializers.py

from rest_framework import serializers
from .models import Service, ServiceAttachment
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

class ServiceAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAttachment
        fields = ['id', 'file', 'uploaded_at', 'filename', 'extension', 'filesize']
        read_only_fields = ['id', 'uploaded_at', 'filename', 'extension', 'filesize']

    def validate_file(self, value):
        if value.size > 25 * 1024 * 1024:  # 25MB limit
            raise serializers.ValidationError("File size cannot exceed 25MB.")
        return value



class ServiceSerializer(serializers.ModelSerializer):
    attachments = ServiceAttachmentSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id', 'title', 'subtitle', 'description', 'sub_description',
            'service_image', 'sub_service_image', 'date_posted', 'created_at',
            'updated_at', 'status', 'created_by', 'attachments', 'slug',
            'meta_title', 'meta_description', 'meta_keywords', 'canonical_url',
            'absolute_url'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'created_by', 'slug', 'absolute_url'
        ]
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value.strip()
    
    
    def validate_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Description is required.")
        return value.strip()
    
    
    def validate_status(self, value):
        if value not in dict(Service.STATUS_CHOICES).keys():
            raise serializers.ValidationError("Invalid status.")
        return value


    def to_representation(self, instance):
        """Custom representation to include attachment URLs"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request:
            # Add full URLs for images
            if instance.service_image:
                representation['service_image'] = request.build_absolute_uri(instance.service_image.url)
            if instance.sub_service_image:
                representation['sub_service_image'] = request.build_absolute_uri(instance.sub_service_image.url)
            
            # Include attachments if they exist
            if instance.attachments.exists():
                representation['attachments'] = ServiceAttachmentSerializer(
                    instance.attachments.all(),
                    many=True,
                    context={'request': request}
                ).data
        
        return representation