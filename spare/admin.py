from django.contrib import admin
from .models import  Item, Vehicle, StoreShelf, Supplier, Purchase, Sell
# Register your models here.

class ItemAdmins(admin.ModelAdmin):
    fields = ('part_number', 'name', 'purchase_price', 'selling_price', 'quantity', 'available_quantity', 'measurment',
     'type_of_car', 'purchase_date', 'shelf', 'image_tag', 'photo')
    readonly_fields = ('image_tag',)
    filter_horizontal = ()
    list_filter = ('shelf', 'type_of_car', 'purchase_date')

admin.site.register(Item, ItemAdmins)
admin.site.register(Vehicle)
admin.site.register(StoreShelf)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(Sell)