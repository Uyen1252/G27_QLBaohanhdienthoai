from django.urls import path
from . import views

urlpatterns = [
    path('', views.phone_list, name='phone_list'),
    path('warranty/', views.warranty_list, name='warranty_list'),
    path('add_phone/', views.add_phone, name='add_phone'),
    path('update_phone/<int:phone_id>/', views.update_phone, name='update_phone'),
    path('delete_phone/<int:phone_id>/', views.delete_phone, name='delete_phone'),
    path('add_warranty/', views.add_warranty, name='add_warranty'),
    path('update_warranty/<int:warranty_id>/', views.update_warranty, name='update_warranty'),
    path('delete_warranty/<int:warranty_id>/', views.delete_warranty, name='delete_warranty'),
    path('search_phone/', views.search_phone, name='search_phone'),
    path('search_warranty/', views.search_warranty, name='search_warranty'),
    path('expired_warranty/', views.expired_warranty, name='expired_warranty'),
    path('high_warranty/', views.high_warranty, name='high_warranty'),
     path('high_warranty_chart/', views.HighWarrantyChartView, name='high_warranty_chart'),
    
]

