
# web_apis/contact/urls.py

from django.urls import path
from .views import ContactSubmissionView, ContactListView, ContactDeleteView

urlpatterns = [
    path('submit/', ContactSubmissionView.as_view(), name='contact-submission'),
    path('contacts/', ContactListView.as_view(), name='contact-list'),
    path('delete/<int:contact_id>/', ContactDeleteView.as_view(), name='contact-delete'), 
]