

# # web_apis/evigdia_services/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ServiceSubmissionView.as_view(), name='service-create'),
    # Endpoint: /api/services/create/
    # Methods: POST
    # Description: Creates a new service. Requires authentication. Accepts form data including title, description, status, optional subtitle and sub_description, service_image, sub_service_image, and multiple attachments.

    path('', views.ServiceListView.as_view(), name='service-list'),
    # Endpoint: /api/services/
    # Methods: GET
    # Description: Retrieves a list of all services. Allows unauthenticated access.

    path('<slug:slug>/', views.ServiceDetailView.as_view(), name='service-detail'),
    # Endpoint: /api/services/<slug>/
    # Methods: GET
    # Description: Retrieves details of a specific service based on its slug. Allows unauthenticated access.

    path('<slug:slug>/update/', views.ServiceUpdateView.as_view(), name='service-update'),
    # Endpoint: /api/services/<slug>/update/
    # Methods: PUT, PATCH
    # Description:
    #   - PUT: Updates all fields of an existing service based on its slug. Requires authentication. Accepts form data similar to the create endpoint.
    #   - PATCH: Partially updates one or more fields of an existing service based on its slug. Requires authentication. Accepts form data similar to the create endpoint, but only the fields to be updated need to be included.

    path('<slug:slug>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),
    # Endpoint: /api/services/<slug>/delete/
    # Methods: DELETE
    # Description: Deletes a specific service based on its slug. Requires admin authentication.
]













# from django.urls import path
# from . import views

# urlpatterns = [
#     path('create/', views.ServiceSubmissionView.as_view(), name='service-create'),
#     # Endpoint: /api/services/create/
#     # Methods: POST
#     # Description: Creates a new service. Requires authentication. Accepts form data including title, description, status, optional subtitle and sub_description, service_image, sub_service_image, and multiple attachments.

#     path('', views.ServiceListView.as_view(), name='service-list'),
#     # Endpoint: /api/services/
#     # Methods: GET
#     # Description: Retrieves a list of all services. Allows unauthenticated access.

#     path('<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
#     # Endpoint: /api/services/<id>/
#     # Methods: GET
#     # Description: Retrieves details of a specific service based on its ID. Allows unauthenticated access.

#     path('<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service-update'),
#     # Endpoint: /api/services/<id>/update/
#     # Methods: PUT, PATCH
#     # Description:
#     #   - PUT: Updates all fields of an existing service based on its ID. Requires authentication. Accepts form data similar to the create endpoint.
#     #   - PATCH: Partially updates one or more fields of an existing service based on its ID. Requires authentication. Accepts form data similar to the create endpoint, but only the fields to be updated need to be included.

#     path('<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),
#     # Endpoint: /api/services/<id>/delete/
#     # Methods: DELETE
#     # Description: Deletes a specific service based on its ID. Requires admin authentication.
# ]











# # web_apis/evigdia_services/urls.py

# # from django.urls import path
# # from . import views

# # urlpatterns = [
# #     path('create/', views.ServiceSubmissionView.as_view(), name='service-create'),
# #     path('', views.ServiceListView.as_view(), name='service-list'),
# #     path('<int:pk>/', views.ServiceDetailView.as_view(), name='service-detail'),
# #     path('<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service-update'),
# #     path('<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service-delete'),
# # ]