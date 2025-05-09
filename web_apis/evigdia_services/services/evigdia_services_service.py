

# web_apis/services/evigdia_services_service.py

import logging
from django.db import transaction
from ..models import Service, ServiceAttachment
from user_account.permissions import IsAdmin
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

class ServiceService:
    @staticmethod
    def create_service(data, files=None, request=None):
        try:
            with transaction.atomic():
                # Add request user as creator
                if request and request.user.is_authenticated:
                    data['created_by'] = request.user

                # Include image files from request (they are already in data)
                service = Service.objects.create(**data)

                # Process attachments
                if files:
                    for file in files:
                        ServiceAttachment.objects.create(
                            service=service,
                            file=file
                        )

                return service, None

        except Exception as e:
            logger.error(f"Error creating service: {str(e)}")
            return None, str(e)


    @staticmethod
    def get_service(identifier, request):
        """Now accepts either slug or pk"""
        try:
            if isinstance(identifier, int) or identifier.isdigit():
                service = Service.objects.get(pk=identifier)
            else:
                service = Service.objects.get(slug=identifier)
            return service, None
        except Service.DoesNotExist:
            return None, "Service not found"
        except Exception as e:
            logger.error(f"Error retrieving service: {str(e)}")
            return None, str(e)
        
    # def get_service(pk, request):
    #     try:
    #         service = Service.objects.get(pk=pk)
    #         return service, None
    #     except Service.DoesNotExist:
    #         return None, "Service not found"
    #     except Exception as e:
    #         logger.error(f"Error retrieving service: {str(e)}")
    #         return None, str(e)

    @staticmethod
    def get_all_services(request):
        try:
            return Service.objects.all().order_by('-date_posted'), None
        except Exception as e:
            logger.error(f"Error retrieving services: {str(e)}")
            return None, str(e)

    @staticmethod
    def update_service(pk, data, files=None, request=None, instance=None):
        try:
            with transaction.atomic():
                service = instance if instance else Service.objects.get(pk=pk)

                # Update fields
                for field, value in data.items():
                    setattr(service, field, value)
                service.save()

                # Process new attachments
                if files:
                    for file in files:
                        ServiceAttachment.objects.create(
                            service=service,
                            file=file
                        )

                return service, None

        except Service.DoesNotExist:
            return None, "Service not found"
        except Exception as e:
            logger.error(f"Error updating service: {str(e)}")
            return None, str(e)

    @staticmethod
    def delete_service(pk, request):
        try:
            service = Service.objects.get(pk=pk)
            if not IsAdmin().has_permission(request, None):
                return False, "Permission denied"

            service.delete()
            return True, None
        except Service.DoesNotExist:
            return False, "Service not found"
        except Exception as e:
            logger.error(f"Error deleting service: {str(e)}")
            return False, str(e)



