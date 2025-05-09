from django.urls import path
from . import views

urlpatterns = [
    # GlobalAppControl CRUD endpoints
    path('global-control/', views.GlobalAppControlView.as_view(), name='global_control_crud'),
    
    # AppManager CRUD endpoints
    path('app-manager/', views.AppManagerView.as_view(), name='app_manager_list_create'),
    path('app-manager/<str:app_type>/', views.AppManagerView.as_view(), name='app_manager_detail'),
    
    # App Status Check endpoint (for desktop clients)
    path('status/', views.AppStatusCheckView.as_view(), name='app_status_check'),
]