

# blog/validators/blog_validators.copy()

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_image_file_extension
from django.utils import timezone

class BlogPostValidator:
    
    @classmethod
    def validate_post_create(cls, data):
        """
        Validates all aspects of post creation
        """
        cls._validate_required_fields(data)
        # cls._validate_content_length(data)
        cls._validate_featured_image(data.get('featured_image'))
        cls._validate_scheduled_date(data)
        cls._validate_seo_fields(data)

    @classmethod
    def validate_post_update(cls, data, instance=None):
        """
        Validates all aspects of post update
        """
        # cls._validate_content_length(data)
        cls._validate_featured_image(data.get('featured_image'))
        cls._validate_scheduled_date(data)
        cls._validate_status_change(data, instance)
        cls._validate_seo_fields(data)

    @classmethod
    def _validate_required_fields(cls, data):
        required_fields = ['title', 'content']
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(
                    _(f"{field} is required for creating a blog post")
                )

    @classmethod
    # def _validate_content_length(cls, data):
    #     content = data.get('content', '')
    #     if len(content.split()) < 200:
    #         raise ValidationError(
    #             _("Blog post content must be at least 200 words")
    #         )

    @classmethod
    def _validate_featured_image(cls, image):
        if image:
            # Validate file type
            try:
                validate_image_file_extension(image)
            except ValidationError:
                raise ValidationError(
                    _("Unsupported image format. Use JPG, PNG or WebP")
                )
            
            # Validate file size (5MB max)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError(
                    _("Featured image size cannot exceed 5MB")
                )

    @classmethod
    def _validate_scheduled_date(cls, data):
        if data.get('status') == 'scheduled' and not data.get('scheduled_at'):
            raise ValidationError(
                _("Scheduled posts must have a scheduled_at date")
            )
        if data.get('scheduled_at'):
            scheduled_at = data['scheduled_at']
            if scheduled_at < timezone.now():
                raise ValidationError(
                    _("Scheduled date must be in the future")
                )

    @classmethod
    def _validate_status_change(cls, data, instance):
        if instance and 'status' in data:
            if (instance.status == 'archived' and 
                data['status'] != 'archived'):
                raise ValidationError(
                    _("Archived posts cannot be directly changed to other statuses")
                )

    @classmethod
    def _validate_seo_fields(cls, data):
        if 'meta_title' in data and data['meta_title']:
            if len(data['meta_title']) > 70:
                raise ValidationError(
                    _("Meta title must be 70 characters or less")
                )
        if 'meta_description' in data and data['meta_description']:
            if len(data['meta_description']) > 160:
                raise ValidationError(
                    _("Meta description must be 160 characters or less")
                )