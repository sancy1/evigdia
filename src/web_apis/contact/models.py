

# web_apis/contact/models.py


import os
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import (
    validate_email,
    FileExtensionValidator,
    MaxValueValidator
)
from django.core.exceptions import ValidationError
from django.utils import timezone
import phonenumbers

def upload_contact_attachment_path(instance, filename):
    """Generates a unique file path for contact attachments."""
    today = timezone.now()
    return f"contact_attachments/{today.year}/{today.month}/{today.day}/{uuid.uuid4()}_{filename}"

class Contact(models.Model):
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('either', 'Either'),
    ]

    URGENCY_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    def validate_international_phone_number(phone_number):
        if not phone_number:
            return
        try:
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise ValidationError("Invalid phone number format.")

    # Basic information
    full_name = models.CharField(max_length=255)
    email = models.EmailField(validators=[validate_email])
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_international_phone_number],
        help_text="International format preferred"
    )

    # Submission details
    subject = models.CharField(max_length=255)
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_METHOD_CHOICES,
        default='email'
    )
    urgency_level = models.CharField(
        max_length=10,
        choices=URGENCY_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    message_content = models.TextField()
    privacy_policy_accepted = models.BooleanField(
        default=False,
        help_text="Required to submit the form"
    )
    
    # Metadata
    submission_date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer_url = models.URLField(blank=True, null=True)
    browser_language = models.CharField(max_length=10, blank=True, null=True)
    
    # Processing fields
    is_processed = models.BooleanField(default=False)
    processed_date = models.DateTimeField(blank=True, null=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='processed_contacts'
    )
    
    # Security
    captcha_token = models.CharField(
        max_length=1000,
        blank=False,
        null=False,
        help_text="CAPTCHA verification token to prevent spam submissions"
    )
    captcha_verified = models.BooleanField(default=False)
    captcha_verified_at = models.DateTimeField(blank=True, null=True)
    recaptcha_score = models.FloatField(blank=True, null=True)
    
    # def verify_recaptcha(self):
    #     """Verify reCAPTCHA token with Google's API"""
    #     if not settings.RECAPTCHA_SECRET_KEY:
    #         self.captcha_verified = True  # Bypass in development
    #         return True
            
    #     data = {
    #         'secret': settings.RECAPTCHA_SECRET_KEY,
    #         'response': self.captcha_token
    #     }
    #     response = requests.post(
    #         'https://www.google.com/recaptcha/api/siteverify',
    #         data=data
    #     )
    #     result = response.json()
        
    #     if result.get('success'):
    #         self.captcha_verified = True
    #         self.recaptcha_score = result.get('score', 0)
    #         return True
    #     return False
    
    # def clean(self):
    #     """Validate CAPTCHA during model validation"""
    #     super().clean()
        
    #     if not self.captcha_token:
    #         raise ValidationError("CAPTCHA verification is required")
            
    #     if not self.verify_recaptcha():
    #         raise ValidationError("CAPTCHA verification failed")
            
    #     # Optional: Check score threshold (e.g., 0.5 for reCAPTCHA v3)
    #     if (self.recaptcha_score is not None and 
    #         self.recaptcha_score < getattr(settings, 'RECAPTCHA_SCORE_THRESHOLD', 0.5)):
    #         raise ValidationError("CAPTCHA verification score too low")


    class Meta:
        ordering = ['-submission_date']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def clean(self):
        if self.preferred_contact_method in ['phone', 'either'] and not self.phone_number:
            raise ValidationError(
                "Phone number is required when preferred contact method is Phone or Either."
            )
        if not self.privacy_policy_accepted:
            raise ValidationError("You must accept the privacy policy.")

    def __str__(self):
        return f"{self.full_name} <{self.email}> - {self.subject}"
    

class ContactAttachment(models.Model):
    contact = models.ForeignKey(
        Contact,
        related_name='attachments',
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=upload_contact_attachment_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt']
            ),
            MaxValueValidator(10 * 1024 * 1024)  # 10MB limit
        ]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.file.name)

    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        return os.path.splitext(self.file.name)[1][1:].lower()

    def filesize(self):
        return self.file.size if self.file else 0

    class Meta:
        verbose_name = "Contact Attachment"
        verbose_name_plural = "Contact Attachments"