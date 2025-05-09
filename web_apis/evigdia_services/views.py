

# web_apis/evigdia_services/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Service
from .serializers import ServiceSerializer
from .services.evigdia_services_service import ServiceService
from .validators.services_validators import ServiceValidator
from user_account.permissions import IsAuthenticated, IsAdmin
from rest_framework.permissions import AllowAny
import logging

logger = logging.getLogger(__name__)

class ServiceSubmissionView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Prepare data
        data = request.data.dict()
        files = request.FILES.getlist('attachments')
        image_file = request.FILES.get('service_image')
        sub_image_file = request.FILES.get('sub_service_image')

        # Validate individual fields
        errors = {}
        validated_data = {}

        title_value, title_error = ServiceValidator.validate_title(data.get('title'))
        if title_error:
            errors['title'] = [title_error]
        else:
            validated_data['title'] = title_value

        description_value, desc_error = ServiceValidator.validate_description(data.get('description'))
        if desc_error:
            errors['description'] = [desc_error]
        else:
            validated_data['description'] = description_value

        status_value, status_error = ServiceValidator.validate_status(data.get('status', 'draft'))
        if status_error:
            errors['status'] = [status_error]
        else:
            validated_data['status'] = status_value

        # Optional fields
        if 'subtitle' in data:
            validated_data['subtitle'] = data['subtitle']
        if 'sub_description' in data:
            validated_data['sub_description'] = data['sub_description']
        if 'meta_title' in data:
            validated_data['meta_title'] = data['meta_title']
        if 'meta_description' in data:
            validated_data['meta_description'] = data['meta_description']
        if 'meta_keywords' in data:
            validated_data['meta_keywords'] = data['meta_keywords']
        if 'canonical_url' in data:
            validated_data['canonical_url'] = data['canonical_url']

        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Include image files in validated data FOR SERIALIZER VALIDATION
        validated_data['service_image'] = image_file
        validated_data['sub_service_image'] = sub_image_file

        serializer = ServiceSerializer(data=validated_data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Serializer validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate files
        file_errors = []
        validated_files = []
        for file in files:
            validated_file, file_error = ServiceValidator.validate_file(file)
            if file_error:
                file_errors.append(file_error)
            else:
                validated_files.append(validated_file)

        if file_errors:
            return Response({
                'status': 'error',
                'message': 'File validation failed',
                'errors': {'attachments': file_errors}
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create service
        service, error = ServiceService.create_service(
            serializer.validated_data, # Pass the validated data which ALREADY includes image files
            files=validated_files,
            request=request
        )

        if error:
            return Response({
                'status': 'error',
                'message': 'Failed to create service',
                'error': error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return response
        response_serializer = ServiceSerializer(service, context={'request': request})
        return Response({
            'status': 'success',
            'message': 'Service created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
        
        
        

class ServiceListView(APIView):
    permission_classes = [AllowAny]  # Allow visitors to GET

    def get(self, request):
        services, error = ServiceService.get_all_services(request)
        if error:
            return Response({
                'status': 'error',
                'message': error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = ServiceSerializer(services, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data
        })



class ServiceDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):  # Changed from pk to slug
        try:
            service = Service.objects.get(slug=slug)
        except Service.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Service not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ServiceSerializer(service, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data
        })



class ServiceUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, slug):
        return self._update(request, slug, partial=False)

    def patch(self, request, slug):
        return self._update(request, slug, partial=True)

    def _update(self, request, slug, partial):
        data = request.data.dict()
        files = request.FILES.getlist('attachments')
        image_file = request.FILES.get('service_image')
        sub_image_file = request.FILES.get('sub_service_image')

        # Validate data
        errors = {}
        validated_data = {}

        if 'title' in data:
            title_value, title_error = ServiceValidator.validate_title(data['title'])
            if title_error:
                errors['title'] = [title_error]
            else:
                validated_data['title'] = title_value

        if 'description' in data:
            desc_value, desc_error = ServiceValidator.validate_description(data['description'])
            if desc_error:
                errors['description'] = [desc_error]
            else:
                validated_data['description'] = desc_value

        if 'status' in data:
            status_value, status_error = ServiceValidator.validate_status(data['status'])
            if status_error:
                errors['status'] = [status_error]
            else:
                validated_data['status'] = status_value

        # Optional fields
        if 'subtitle' in data:
            validated_data['subtitle'] = data['subtitle']
        if 'sub_description' in data:
            validated_data['sub_description'] = data['sub_description']

        # Include image files for update as well
        if image_file:
            validated_data['service_image'] = image_file
        if sub_image_file:
            validated_data['sub_service_image'] = sub_image_file

        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate files
        file_errors = []
        validated_files = []
        for file in files:
            validated_file, file_error = ServiceValidator.validate_file(file)
            if file_error:
                file_errors.append(file_error)
            else:
                validated_files.append(validated_file)

        if file_errors:
            return Response({
                'status': 'error',
                'message': 'File validation failed',
                'errors': {'attachments': file_errors}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = Service.objects.get(slug=slug)  # Changed from pk to slug
        except Service.DoesNotExist:
            return Response({'status': 'error', 'message': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceSerializer(service, data=validated_data, partial=partial, context={'request': request})
        if serializer.is_valid():
            updated_service, error = ServiceService.update_service(
                service.id,  # Still pass ID to service layer
                serializer.validated_data,
                files=validated_files,
                request=request,
                instance=service
            )
            if error:
                return Response({'status': 'error', 'message': error}, status=status.HTTP_400_BAD_REQUEST)
            response_serializer = ServiceSerializer(updated_service, context={'request': request})
            return Response({
                'status': 'success',
                'message': f'Service {"partially " if partial else ""}updated successfully',
                'data': response_serializer.data
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Serializer validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
        
class ServiceDeleteView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, slug):  # Changed from pk to slug
        try:
            service = Service.objects.get(slug=slug)
            if not IsAdmin().has_permission(request, None):
                return Response({
                    'status': 'error',
                    'message': 'Permission denied'
                }, status=status.HTTP_403_FORBIDDEN)

            service.delete()
            return Response({
                'status': 'success',
                'message': 'Service deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Service.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Service not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting service: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


