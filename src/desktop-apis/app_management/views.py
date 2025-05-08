# views.py
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.permissions import AllowAny
from .models import AppManager, GlobalAppControl

from .serializers import (
    AppManagerSerializer, 
    GlobalAppControlSerializer,
    AppStatusSerializer,
)

from .swagger_docs import (
    global_app_control_post_schema,
    global_app_control_get_schema,
    global_app_control_put_schema,
    global_app_control_patch_schema,
    global_app_control_delete_schema,
    app_manager_delete_schema, 
    app_manager_patch_schema,
    app_manager_put_schema, 
    app_manager_get_schema,      
    app_manager_post_schema, 
    app_status_check_schema,
)

logger = logging.getLogger(__name__)

class APIKeyValidator:
    permission_classes = [AllowAny]
    @staticmethod
    def validate(request):
        api_key = request.data.get('api_key')
        if not api_key:
            logger.warning("API key missing in request")
            return Response(
                {"error": "api_key parameter is required in the request body"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if api_key != settings.APP_MANAGEMENT_API_KEY:
            logger.warning(f"Invalid API key attempt: {api_key}")
            return Response(
                {"error": "Invalid API key"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return None



# Global Control ------------------------------------------------------------------------------------
class GlobalAppControlView(APIView):
    """Complete CRUD for GlobalAppControl"""
    permission_classes = [AllowAny]
    
    
    @global_app_control_post_schema()
    def post(self, request):
        """Create new global control"""
        if error := APIKeyValidator.validate(request):
            return error
            
        # Ensure only one instance exists
        if GlobalAppControl.objects.exists():
            return Response(
                {"error": "Global control already exists. Use PUT/PATCH to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = GlobalAppControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @global_app_control_get_schema()
    def get(self, request):
        """Get current global control"""
        if error := APIKeyValidator.validate(request):
            return error
            
        control = GlobalAppControl.objects.first()
        if not control:
            control = GlobalAppControl.objects.create()
        serializer = GlobalAppControlSerializer(control)
        return Response(serializer.data)
    

    @global_app_control_put_schema()
    def put(self, request):
        """Full update of global control"""
        if error := APIKeyValidator.validate(request):
            return error
            
        control = GlobalAppControl.objects.first()
        if not control:
            control = GlobalAppControl.objects.create()
            
        serializer = GlobalAppControlSerializer(control, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @global_app_control_patch_schema()
    def patch(self, request):
        """Partial update of global control"""
        if error := APIKeyValidator.validate(request):
            return error
            
        control = GlobalAppControl.objects.first()
        if not control:
            control = GlobalAppControl.objects.create()
            
        serializer = GlobalAppControlSerializer(control, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @global_app_control_delete_schema()
    def delete(self, request):
        """Delete global control (will recreate on next access)"""
        if error := APIKeyValidator.validate(request):
            return error
            
        GlobalAppControl.objects.all().delete()
        return Response(
            {"message": "Global control deleted. A new one will be created when needed."},
            status=status.HTTP_204_NO_CONTENT
        )



# APP Management ------------------------------------------------------------------------------------
class AppManagerView(APIView):
    """Complete CRUD for AppManager"""
    permission_classes = [AllowAny]
    
    @app_manager_post_schema()
    def post(self, request):
        """Create new app manager"""
        if error := APIKeyValidator.validate(request):
            return error
            
        app_type = request.data.get('app_type')
        if not app_type:
            return Response(
                {"error": "app_type is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if AppManager.objects.filter(app_type=app_type).exists():
            return Response(
                {"error": f"App manager for {app_type} already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = AppManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @app_manager_get_schema()
    def get(self, request, app_type=None):
        """Get app manager(s)"""
        if error := APIKeyValidator.validate(request):
            return error
            
        if app_type:
            manager = get_object_or_404(AppManager, app_type=app_type)
            serializer = AppManagerSerializer(manager)
            return Response(serializer.data)
        
        managers = AppManager.objects.all()
        serializer = AppManagerSerializer(managers, many=True)
        return Response(serializer.data)



    @app_manager_put_schema()
    def put(self, request, app_type):
        """Full update of app manager"""
        if error := APIKeyValidator.validate(request):
            return error
            
        manager = get_object_or_404(AppManager, app_type=app_type)
        serializer = AppManagerSerializer(manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @app_manager_patch_schema()
    def patch(self, request, app_type):
        """Partial update of app manager"""
        if error := APIKeyValidator.validate(request):
            return error
            
        manager = get_object_or_404(AppManager, app_type=app_type)
        serializer = AppManagerSerializer(manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @app_manager_delete_schema()
    def delete(self, request, app_type):
        """Delete app manager"""
        
        if error := APIKeyValidator.validate(request):
            return error
            
        manager = get_object_or_404(AppManager, app_type=app_type)
        manager.delete()
        return Response(
            {"message": f"App manager for {app_type} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )




# APP Satus ------------------------------------------------------------------------------------
class AppStatusCheckView(APIView):
    permission_classes = [AllowAny]
    
    @app_status_check_schema()
    def post(self, request):
        api_key = request.data.get('api_key')
        
        if not api_key:
            return Response(
                {"error": "api_key parameter is required in the request body"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if api_key != settings.APP_MANAGEMENT_API_KEY:
            logger.warning(f"Invalid API key: {api_key}")
            return Response(
                {"error": "Invalid API key"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = AppStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        app_types = data.get('app_types', [])
        
        # Check global status first
        global_control = GlobalAppControl.objects.first()
        if not global_control:
            global_control = GlobalAppControl.objects.create()
        
        response_data = {
            'global': {
                'is_shutdown': global_control.is_global_shutdown,
                'shutdown_message': global_control.global_shutdown_message,
                'requires_update': global_control.is_global_update,
                'update_message': global_control.global_update_message,
                'website_url': global_control.website_url,
            },
            'apps': {}
        }
        
        # If global shutdown, we don't need to check individual apps
        if global_control.is_global_shutdown:
            return Response(response_data)
        
        # Get status for requested apps (or all if none specified)
        if app_types:
            managers = AppManager.objects.filter(app_type__in=app_types)
        else:
            managers = AppManager.objects.all()
        
        for manager in managers:
            response_data['apps'][manager.app_type] = {
                'is_active': manager.is_active,
                'requires_update': manager.requires_update,
                'shutdown_message': manager.shutdown_message,
                'update_message': manager.update_message,
                'website_url': manager.website_url,
            }
        
        return Response(response_data)