

# web_apis/contact/services/contact_service.py

import logging
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from ..models import Contact, ContactAttachment
from django.utils import timezone
from user_account.permissions import IsAdmin

logger = logging.getLogger(__name__)

class ContactService:
    @staticmethod
    def create_contact(data, files=None, request=None):
        try:
            with transaction.atomic():
                # Add request metadata
                if request:
                    data.update({
                        'ip_address': request.META.get('REMOTE_ADDR'),
                        'user_agent': request.META.get('HTTP_USER_AGENT'),
                        'referrer_url': request.META.get('HTTP_REFERER'),
                        'browser_language': request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:10],
                    })

                # Create contact first
                contact = Contact.objects.create(**data)

                # Process attachments separately
                if files:
                    for file in files:
                        ContactAttachment.objects.create(
                            contact=contact,  # This properly sets the foreign key
                            file=file
                        )

                return contact, None

        except Exception as e:
            logger.error(f"Error creating contact: {str(e)}")
            return None, str(e)

    @staticmethod
    def get_contact(pk, request):
        """
        Retrieves a single contact submission with permission check
        """
        try:
            contact = Contact.objects.get(pk=pk)
            if not IsAdmin().has_permission(request, None):
                return None, "Permission denied"
            return contact, None
        except Contact.DoesNotExist:
            return None, "Contact not found"
        except Exception as e:
            logger.error(f"Error retrieving contact: {str(e)}")
            return None, str(e)

    @staticmethod
    def get_all_contacts(request):
        """
        Retrieves all contacts (admin only)
        """
        if not IsAdmin().has_permission(request, None):
            return None, "Permission denied"
        try:
            return Contact.objects.all().order_by('-submission_date'), None
        except Exception as e:
            logger.error(f"Error retrieving contacts: {str(e)}")
            return None, str(e)

    @staticmethod
    def delete_contact(pk, request):
        """
        Deletes a contact submission (admin only)
        """
        try:
            contact = Contact.objects.get(pk=pk)
            if not IsAdmin().has_permission(request, None):
                return False, "Permission denied"
            
            contact.delete()
            return True, None
        except Contact.DoesNotExist:
            return False, "Contact not found"
        except Exception as e:
            logger.error(f"Error deleting contact: {str(e)}")
            return False, str(e)
        
        

    @staticmethod
    def delete_contact(contact_id, request):
        try:
            contact = Contact.objects.get(pk=contact_id)
            contact.delete()  # Perform permanent delete
            logger.info(f"Contact {contact_id} permanently deleted by {request.user}")
            return True, None
        except Contact.DoesNotExist:
            return False, "Contact submission not found"
        except Exception as e:
            logger.error(f"Error deleting contact {contact_id}: {e}")
            return False, str(e)