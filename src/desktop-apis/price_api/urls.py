
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('price/', views.get_price, name='get_price'),
#     path('price/update/', views.update_price),
    
# ]


# price_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('price/', views.get_price, name='get_price'),
    path('price/update/', views.update_price, name='update_price'),
    path('plans/<str:plan_type>/', views.get_plan, name='get_plan'),
    path('plans/', views.get_all_plans, name='get_all_plans'),
    path('create/', views.create_price, name='create_price'),
    
    path('deactivate/<str:plan_type>/', views.deactivate_plan, name='deactivate_plan'),
    path('reactivate/<str:plan_type>/', views.reactivate_plan, name='reactivate_plan'),
]