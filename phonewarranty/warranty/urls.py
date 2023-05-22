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
    path('TK/', views.TK, name='TK'),
    path('ajax/get-names-by-brand/', views.ajax_get_names_by_brand, name='ajax_get_names_by_brand'),
    path('ajax/ajax_get_names_by_ncc/', views.ajax_get_names_by_ncc, name='ajax_get_names_by_ncc'),
    path('ajax/ajax_get_names_by_brand_and_ncc/', views.ajax_get_names_by_brand_and_ncc, name='ajax_get_names_by_brand_and_ncc'),
    path('ajax/get-all-names/', views.ajax_get_all_names, name='ajax_get_all_names'),
    path('ajax/ajax_get_names_by_warranty_status', views.ajax_get_names_by_warranty_status, name='ajax_get_names_by_warranty_status'),
    path('ajax/ajax_get_names_by_brand_and_warranty_status', views.ajax_get_names_by_brand_and_warranty_status, name='ajax_get_names_by_brand_and_warranty_status'),
    path('ajax/ajax_get_names_by_ncc_and_warranty_status', views.ajax_get_names_by_ncc_and_warranty_status, name='ajax_get_names_by_ncc_and_warranty_status'),
    path('ajax/ajax_get_names_by_brand_ncc_and_warranty_status', views.ajax_get_names_by_brand_ncc_and_warranty_status, name='ajax_get_names_by_brand_ncc_and_warranty_status'),
    path('TK_baohanh/', views.TK_baohanh, name='TK_baohanh'),
    path('ajax/get-names-by-brand_baohanh/', views.ajax_get_names_by_brand_baohanh, name='ajax_get_names_by_brand_baohanh'),
    path('ajax/ajax_get_names_by_ncc_baohanh/', views.ajax_get_names_by_ncc_baohanh, name='ajax_get_names_by_ncc_baohanh'),
    path('ajax/ajax_get_names_by_brand_and_ncc_baohanh/', views.ajax_get_names_by_brand_and_ncc_baohanh, name='ajax_get_names_by_brand_and_ncc_baohanh'),
    path('ajax/get-all-names_baohanh/', views.ajax_get_all_names_baohanh, name='ajax_get_all_names_baohanh'),   
    path('phone-autocomplete/', PhoneAutocomplete.as_view(), name='phone-autocomplete'),
]
