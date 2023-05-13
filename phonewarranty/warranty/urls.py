from django.urls import path
from . import views
from .views import PhoneAutocomplete


urlpatterns = [
    path('register', views.register, name='register'),
    path("", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path('phone_list', views.phone_list, name='phone_list'),
    path('warranty_list/', views.warranty_list, name='warranty_list'),
    path('add_phone/', views.add_phone, name='add_phone'),
    path('update_phone/<int:phone_id>/', views.update_phone, name='update_phone'),
    path('delete_phone/<int:phone_id>/', views.delete_phone, name='delete_phone'),
    path('search_phone/', views.search_phone, name='search_phone'),
    path('add_warranty/', views.add_warranty, name='add_warranty'),
    path('update_warranty/<int:warranty_id>/', views.update_warranty, name='update_warranty'),
    path('delete_warranty/<int:warranty_id>/', views.delete_warranty, name='delete_warranty'),
    path('search_warranty/', views.search_warranty, name='search_warranty'),
    path('ajax/get-names-by-brand/', views.ajax_get_names_by_brand, name='ajax_get_names_by_brand'),
    path('ajax/get-all-names/', views.ajax_get_all_names, name='ajax_get_all_names'),
    path('TK/', views.TK, name='TK'),
    path('phone-autocomplete/', PhoneAutocomplete.as_view(), name='phone-autocomplete'),
]
