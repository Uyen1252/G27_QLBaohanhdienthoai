from django.urls import path
from . import views

urlpatterns = [
    path('', views.phone_list, name='phone_list'),
    path('phones/<int:pk>/', views.warranty_detail, name='warranty_detail'),
    path('customer/', views.customer_list, name='customer_list'),
    path('add_phone/', views.add_phone, name='add_phone'),
    path('add_warranty/<int:phone_id>/', views.add_warranty, name='add_warranty'),
]

