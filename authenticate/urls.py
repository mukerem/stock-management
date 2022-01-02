from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('homepage/', views.stock_homepage, name='stock_homepage'),
    path('seller/index/', views.seller_index, name='seller_index'),
    path('manager/index/', views.manager_index, name='manager_index'),
    path('profile/', views.view_profile, name='user_view_profile'),
    path('profile/password/', views.change_password, name='change_password'),
    path('supplier/list/', views.supplier_list, name='supplier_list'),
    path('supplier/register/', views.supplier_register, name='supplier_register'),
    path('supplier/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('supplier/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('supplier/delete-done/<int:supplier_id>/', views.delete_supplier_done, name='delete_supplier_done'),
    path('seller/list/', views.seller_list, name='seller_list'),
    path('seller/register/', views.seller_register, name='seller_register'),
    path('seller/edit/<int:seller_id>/', views.edit_seller, name='edit_seller'),
    path('seller/delete/<int:seller_id>/', views.delete_seller, name='delete_seller'),
    path('seller/delete-done/<int:seller_id>/', views.delete_seller_done, name='delete_seller_done'),

]