from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('item/list/', views.stock_item, name='stock_item'),
    path('item/register/', views.item_register, name='item_register'),
    path('item/edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('item/delete-done/<int:item_id>/', views.delete_item_done, name='delete_item_done'),
    path('new-sell/', views.new_sell, name='new_sell'),
    path('sell-list/<str:date>/', views.item_sell_list, name='item_sell_list'),
    path('sell/edit/<int:sell_id>/', views.edit_sell, name='edit_sell'),
    path('sell/delete/<int:sell_id>/', views.delete_sell, name='delete_sell'),
    path('sell/delete-done/<int:sell_id>/', views.delete_sell_done, name='delete_sell_done'),
    path('sell/search-by-date/', views.sell_search_by_date, name='sell_search_by_date'),
    path('purchase/search-by-date/', views.purchase_search_by_date, name='purchase_search_by_date'),
    path('item/select/<int:item_id>/', views.select_item_to_sell, name='select_item_to_sell'),
    path('new-purchase/', views.new_purchase, name='new_purchase'),
    path('purchase-list/<str:date>/', views.item_purchase_list, name='item_purchase_list'),
    path('purchase/edit/<int:purchase_id>/', views.edit_purchase, name='edit_purchase'),
    path('purchase/delete/<int:purchase_id>/', views.delete_purchase, name='delete_purchase'),
    path('purchase/delete-done/<int:purchase_id>/', views.delete_purchase_done, name='delete_purchase_done'),
    path('shelf/list/', views.shelf_list, name='shelf_list'),
    path('shelf/register/', views.shelf_register, name='shelf_register'),
    path('shelf/edit/<int:shelf_id>/', views.edit_shelf, name='edit_shelf'),
    path('shelf/delete/<int:shelf_id>/', views.delete_shelf, name='delete_shelf'),
    path('shelf/delete-done/<int:shelf_id>/', views.delete_shelf_done, name='delete_shelf_done'),
    path('vehicle/list/', views.vehicle_list, name='vehicle_list'),
    path('vehicle/register/', views.vehicle_register, name='vehicle_register'),
    path('vehicle/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('vehicle/delete-done/<int:vehicle_id>/', views.delete_vehicle_done, name='delete_vehicle_done'),
    path('capital/', views.capital, name='capital'),
    path('item/search/', views.search_item, name='search_item'),
    path('item/empty/', views.empty_item, name='empty_item'),
    path('item/sell-ajax-update/', views.ajax_update_sell_data, name='ajax_update_sell_data'),
    path('item/purchase-ajax-update/', views.ajax_update_purchase_data, name='ajax_update_purchase_data'),
    path('sell/vat/<str:date>/', views.vat_sell_list, name='vat_sell_list'),
    path('item/store/', views.store_item_list, name='store_item_list'),
    path('item/move/', views.store_item_move, name='store_item_move'),

]