

# web_apis/contact/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from web_apis.contact.models import Contact
from .serializers import ContactSerializer, ContactAttachmentSerializer
from .services.contact_service import ContactService
from .validators.contact_validator import ContactValidator
from user_account.permissions import IsAdmin
from rest_framework.permissions import AllowAny 
import logging

logger = logging.getLogger(__name__)

class ContactSubmissionView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request):
        # Prepare data
        data = request.data.dict()
        files = request.FILES.getlist('attachments')

        # Validate individual fields
        errors = {}
        validated_data = {}

        full_name_value, full_name_error = ContactValidator.validate_full_name(data.get('full_name'))
        if full_name_error:
            errors['full_name'] = [full_name_error]
        else:
            validated_data['full_name'] = full_name_value

        subject_value, subject_error = ContactValidator.validate_subject(data.get('subject'))
        if subject_error:
            errors['subject'] = [subject_error]
        else:
            validated_data['subject'] = subject_value

        email_value, email_error = ContactValidator.validate_email(data.get('email'))
        if email_error:
            errors['email'] = [email_error]
        else:
            validated_data['email'] = email_value

        phone_value, phone_error = ContactValidator.validate_phone_number(data.get('phone_number'))
        if phone_error:
            errors['phone_number'] = [phone_error]
        else:
            validated_data['phone_number'] = phone_value

        message_value, message_error = ContactValidator.validate_message_content(data.get('message_content'))
        if message_error:
            errors['message_content'] = [message_error]
        else:
            validated_data['message_content'] = message_value

        privacy_value, privacy_error = ContactValidator.validate_privacy_policy(
            data.get('privacy_policy_accepted', False)
        )
        if privacy_error:
            errors['privacy_policy_accepted'] = [privacy_error]
        else:
            validated_data['privacy_policy_accepted'] = privacy_value

        contact_data, contact_error = ContactValidator.validate_contact_method(data)
        if contact_error:
            errors['preferred_contact_method'] = [contact_error] # Assuming the error relates to the preferred method or phone
        else:
            validated_data.update({
                'preferred_contact_method': contact_data.get('preferred_contact_method'),
                'phone_number': contact_data.get('phone_number')
            })

        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContactSerializer(data=validated_data, context={'request': request})
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
            validated_file, file_error = ContactValidator.validate_file(file)
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

        # Create contact and attachments
        contact, error = ContactService.create_contact(
            serializer.validated_data,
            files=validated_files,
            request=request
        )

        if error:
            return Response({
                'status': 'error',
                'message': 'Failed to create contact',
                'error': error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return response with attachment info
        contact_from_db = Contact.objects.get(pk=contact.id) # Refetch the model instance

        # Serialize the model instance to get the representation with attachments
        response_serializer = ContactSerializer(contact_from_db, context={'request': request})

        return Response({
            'status': 'success',
            'message': 'Contact submitted successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    


class ContactListView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        contacts, error = ContactService.get_all_contacts(request)
        if error:
            return Response({
                'status': 'error',
                'message': error
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ContactSerializer(contacts, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data
        })
        


    

# web_apis/contact/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from web_apis.contact.models import Contact
from .serializers import ContactSerializer, ContactAttachmentSerializer
from .services.contact_service import ContactService
from .validators.contact_validator import ContactValidator
from user_account.permissions import IsAdmin
from rest_framework.permissions import AllowAny 
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ContactSubmissionView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request):
        # Prepare data
        data = request.data.dict()
        files = request.FILES.getlist('attachments')

        # Validate individual fields
        errors = {}
        validated_data = {}

        full_name_value, full_name_error = ContactValidator.validate_full_name(data.get('full_name'))
        if full_name_error:
            errors['full_name'] = [full_name_error]
        else:
            validated_data['full_name'] = full_name_value

        subject_value, subject_error = ContactValidator.validate_subject(data.get('subject'))
        if subject_error:
            errors['subject'] = [subject_error]
        else:
            validated_data['subject'] = subject_value

        email_value, email_error = ContactValidator.validate_email(data.get('email'))
        if email_error:
            errors['email'] = [email_error]
        else:
            validated_data['email'] = email_value

        phone_value, phone_error = ContactValidator.validate_phone_number(data.get('phone_number'))
        if phone_error:
            errors['phone_number'] = [phone_error]
        else:
            validated_data['phone_number'] = phone_value

        message_value, message_error = ContactValidator.validate_message_content(data.get('message_content'))
        if message_error:
            errors['message_content'] = [message_error]
        else:
            validated_data['message_content'] = message_value

        privacy_value, privacy_error = ContactValidator.validate_privacy_policy(
            data.get('privacy_policy_accepted', False)
        )
        if privacy_error:
            errors['privacy_policy_accepted'] = [privacy_error]
        else:
            validated_data['privacy_policy_accepted'] = privacy_value

        contact_data, contact_error = ContactValidator.validate_contact_method(data)
        if contact_error:
            errors['preferred_contact_method'] = [contact_error] # Assuming the error relates to the preferred method or phone
        else:
            validated_data.update({
                'preferred_contact_method': contact_data.get('preferred_contact_method'),
                'phone_number': contact_data.get('phone_number')
            })

        if errors:
            return Response({
                'status': 'error',
                'message': 'Validation failed',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ContactSerializer(data=validated_data, context={'request': request})
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
            validated_file, file_error = ContactValidator.validate_file(file)
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

        # Create contact and attachments
        contact, error = ContactService.create_contact(
            serializer.validated_data,
            files=validated_files,
            request=request
        )

        if error:
            return Response({
                'status': 'error',
                'message': 'Failed to create contact',
                'error': error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return response with attachment info
        contact_from_db = Contact.objects.get(pk=contact.id) # Refetch the model instance

        # Serialize the model instance to get the representation with attachments
        response_serializer = ContactSerializer(contact_from_db, context={'request': request})

        return Response({
            'status': 'success',
            'message': 'Contact submitted successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    


class ContactListView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        contacts, error = ContactService.get_all_contacts(request)
        if error:
            return Response({
                'status': 'error',
                'message': error
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ContactSerializer(contacts, many=True, context={'request': request})
        return Response({
            'status': 'success',
            'data': serializer.data
        })
        


class ContactDeleteView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, contact_id):
        deleted, error = ContactService.delete_contact(contact_id, request)
        if error:
            return Response({
                'status': 'error',
                'message': error
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'status': 'success',
            'message': f'Contact with ID {contact_id} deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)





