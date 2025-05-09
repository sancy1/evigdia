

# web_apis/contact/serializers.py

# web_apis/contact/serializers.py
from rest_framework import serializers
from .models import Contact, ContactAttachment
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
import phonenumbers



class ContactAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactAttachment
        fields = ['id', 'file', 'uploaded_at', 'filename', 'extension', 'filesize']
        read_only_fields = ['id', 'uploaded_at', 'filename', 'extension', 'filesize']

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        return value



class ContactSerializer(serializers.ModelSerializer):
    # Remove the attachments field from the serializer
    class Meta:
        model = Contact
        fields = [
            'id', 'full_name', 'email', 'phone_number', 'subject',
            'preferred_contact_method', 'urgency_level', 'message_content',
            'privacy_policy_accepted',
            'ip_address', 'user_agent', 'referrer_url', 'browser_language',
            'submission_date', 'is_processed'
        ]
        read_only_fields = [
            'id', 'ip_address', 'user_agent', 'referrer_url',
            'browser_language', 'submission_date', 'is_processed'
        ]

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value.lower()

    def validate_phone_number(self, value):
        if not value:  # Phone is optional
            return value
            
        try:
            parsed = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(parsed):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        
        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    def validate_message_content(self, value):
        min_length = 20
        if len(value.strip()) < min_length:
            raise serializers.ValidationError(
                f"Message must be at least {min_length} characters long."
            )
        return value

    def validate_privacy_policy_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the privacy policy to submit this form."
            )
        return value

    def validate(self, data):
        # Cross-field validation
        preferred_method = data.get('preferred_contact_method')
        phone_number = data.get('phone_number')
        
        if preferred_method in ['phone', 'either'] and not phone_number:
            raise serializers.ValidationError(
                {"phone_number": "Phone number is required for selected contact method."}
            )
            
        return data

    def create(self, validated_data):
        attachments_data = []
        if 'attachments' in validated_data:
            attachments_data = validated_data.pop('attachments')
        
        # Add metadata from request
        request = self.context.get('request')
        if request:
            validated_data.update({
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT'),
                'referrer_url': request.META.get('HTTP_REFERER'),
                'browser_language': request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:10],
            })
        
        # Create contact instance
        contact = Contact.objects.create(**validated_data)
        
        # Create attachments
        for attachment_data in attachments_data:
            ContactAttachment.objects.create(
                contact=contact,
                file=attachment_data['file']
            )
        
        return contact

    def to_representation(self, instance):
        """Custom representation to include attachment URLs"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if request and instance.attachments.exists():
            representation['attachments'] = ContactAttachmentSerializer(
                instance.attachments.all(),
                many=True,
                context={'request': request}
            ).data
        
        return representation