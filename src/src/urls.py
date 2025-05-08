
# src/urls.py  | main project urls

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from user_account.views import GoogleLogin
from user_account.views import GoogleLogin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from django.contrib import admin
from django.urls import path, include

schema_view = swagger_get_schema_view(
    openapi.Info(
        title='FusionPex API',
        default_version='1.0.0',
        description='API documentation of FussionPex',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fusionpex.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger Documentation -----------------------------------------------------------------------------------------
    path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    
    # Plan and Prices -----------------------------------------------------------------------------------------
    path('api/prices/', include('desktop-apis.price_api.urls')),
    
    # Desktop App Management -----------------------------------------------------------------------------------------
    path('api/app-management/', include('desktop-apis.app_management.urls')),
    
    # Blog -----------------------------------------------------------------------------------------
    path('api/blog/', include('web_apis.blog.urls.blog_urls')),
    
    # Contact (new addition) -----------------------------------------------------------------------------------------
    path('api/contact/', include('web_apis.contact.urls')),
    
    # Services API ----------------------------------------------------------------------------------------------------
    path('api/services/', include('web_apis.evigdia_services.urls')),
    
    # Account -----------------------------------------------------------------------------------------
    path('api/user/', include('user_account.users_urls')),
    path('api/auth/google/', GoogleLogin.as_view(), name='google-login'),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

