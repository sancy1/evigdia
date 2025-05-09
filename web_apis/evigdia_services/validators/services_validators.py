 

 # web_apis/services/validators/services_validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class ServiceValidator:
    @staticmethod
    def validate_title(value):
        if not value or not value.strip():
            return None, _("Title is required.")
        return value.strip(), None

    @staticmethod
    def validate_description(value):
        if not value or not value.strip():
            return None, _("Description is required.")
        return value.strip(), None

    @staticmethod
    def validate_status(value):
        valid_statuses = ['draft', 'published', 'archived', 'pending', 'in_progress', 'completed']
        if value not in valid_statuses:
            return None, _("Invalid status value.")
        return value, None

    @staticmethod
    def validate_file(file):
        max_size = 25 * 1024 * 1024  # 25MB
        allowed_types = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'xls', 'xlsx', 'ppt', 'pptx']
        
        if file.size > max_size:
            return None, _("File size cannot exceed 25MB.")
            
        ext = file.name.split('.')[-1].lower()
        if ext not in allowed_types:
            return None, _("Unsupported file type.")
            
        return file, None