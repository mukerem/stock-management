from django import forms
from .models import Item, Sell, Purchase, StoreShelf, Vehicle
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import check_password
from django.contrib.admin.widgets import FilteredSelectMultiple
from datetime import datetime
from django.forms import ChoiceField
from django.db.models import Q


class EditItem(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'

        widgets = {
            'type_of_car': FilteredSelectMultiple(('tags'), is_stacked=False),
            'shelf': FilteredSelectMultiple(('tags'), is_stacked=False),
        } 
    def clean(self):
        cleaned_data = super().clean()
        part_number = cleaned_data.get('part_number')
        name = cleaned_data.get('name')
        purchase_price = str(cleaned_data.get('purchase_price'))
        selling_price = str(cleaned_data.get('selling_price'))
        quantity = str(cleaned_data.get('quantity'))
        available_quantity = str(cleaned_data.get('available_quantity'))
        measurment = cleaned_data.get('measurment')
        purchase_date = cleaned_data.get('purchase_date')
        type_of_car = cleaned_data.get('type_of_car')
        shelf = cleaned_data.get('shelf')
        if (not part_number) or (not name) or (not purchase_price) or (not selling_price) or (not quantity)\
            or (not available_quantity) or (not measurment) or (not purchase_date) or (not type_of_car) or (not shelf):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data



class ItemRegister(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['available_quantity']

        widgets = {
            'type_of_car': FilteredSelectMultiple(('tags'), is_stacked=False),
            'shelf': FilteredSelectMultiple(('tags'), is_stacked=False),
        } 

    def clean(self):
        cleaned_data = super().clean()
        part_number = cleaned_data.get('part_number')
        name = cleaned_data.get('name')
        purchase_price = str(cleaned_data.get('purchase_price'))
        selling_price = str(cleaned_data.get('selling_price'))
        quantity = str(cleaned_data.get('quantity'))
        measurment = cleaned_data.get('measurment')
        purchase_date = cleaned_data.get('purchase_date')
        type_of_car = cleaned_data.get('type_of_car')
        shelf = cleaned_data.get('shelf')
        if (not part_number) or (not name) or (not purchase_price) or (not selling_price) or (not quantity)\
            or (not measurment) or (not purchase_date) or (not type_of_car) or (not shelf):
            raise forms.ValidationError("Please correct the errors below.")

        return cleaned_data



class NewSell(forms.ModelForm):
    class Meta:
        model = Sell
        exclude = ['seller']

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        selling_price = str(cleaned_data.get('selling_price'))
        date = cleaned_data.get('date')

        if (not item) or (not quantity) or (not selling_price) or (not date):
            raise forms.ValidationError("Please correct the errors below.")
        if quantity > item.available_quantity:
            raise forms.ValidationError("There is only %s available quantity." % str(item.available_quantity))
        return cleaned_data


class EditSell(forms.ModelForm):
    class Meta:
        model = Sell
        exclude = ['seller']

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        selling_price = str(cleaned_data.get('selling_price'))
        date = cleaned_data.get('date')
        if (not item) or (not quantity) or (not selling_price) or (not date):
            raise forms.ValidationError("Please correct the errors below.")
        if quantity > item.available_quantity + self.instance.quantity:
            raise forms.ValidationError("There is only %s available quantity." % str(item.available_quantity + self.instance.quantity))
        return cleaned_data


class NewPurchase(forms.ModelForm):
    stock_quantity = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=0,
        required=True,
        initial=0,
    )
    store_quantity = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=0,
        required=True,
        initial=0,
    )
    class Meta:
        model = Purchase
        fields = ['item', 'quantity', 'supplier', 'purchase_price', 'selling_price', 'stock_quantity', 'store_quantity', 'date']

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        supplier = cleaned_data.get('supplier')
        selling_price = cleaned_data.get('selling_price')
        purchase_price = cleaned_data.get('purchase_price')
        store_quantity = cleaned_data.get('store_quantity')
        stock_quantity = cleaned_data.get('stock_quantity')
        date = cleaned_data.get('date')
        if (not item) or (not str(quantity)) or (not str(purchase_price)) or (not str(selling_price)) or \
            (not str(stock_quantity)) or (not str(store_quantity)) or (not supplier) or (not date):
            raise forms.ValidationError("Please correct the errors below.")

        if store_quantity + stock_quantity != quantity:
            raise forms.ValidationError("total quantity must be equal to the summation of stock quantity and store quantity.")
        return cleaned_data
    
class EditPurchase(forms.ModelForm):
    stock_quantity = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=0,
        required=True,
        initial=0,
    )
    store_quantity = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=0,
        required=True,
        initial=0,
    )
    class Meta:
        model = Purchase
        fields = ['item', 'quantity', 'supplier', 'purchase_price', 'selling_price', 'stock_quantity', 'store_quantity', 'date']

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('item')
        quantity = cleaned_data.get('quantity')
        supplier = cleaned_data.get('supplier')
        selling_price = cleaned_data.get('selling_price')
        purchase_price = cleaned_data.get('purchase_price')
        store_quantity = cleaned_data.get('store_quantity')
        stock_quantity = cleaned_data.get('stock_quantity')
        date = cleaned_data.get('date')
        if (not item) or (not str(quantity)) or (not str(purchase_price)) or (not str(selling_price)) or \
            (not str(stock_quantity)) or (not str(store_quantity)) or (not supplier) or (not date):
            raise forms.ValidationError("Please correct the errors below.")

        if store_quantity + stock_quantity != quantity:
            raise forms.ValidationError("total quantity must be equal to the summation of stock quantity and store quantity.")
        return cleaned_data
    

class ShelfRegister(forms.ModelForm):
    class Meta:
        model = StoreShelf
        fields = '__all__'


class EditShelf(forms.ModelForm):
    class Meta:
        model = StoreShelf
        fields = '__all__'


class VehicleRegister(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class EditVehicle(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class DateSearchEngine(forms.Form):
    search_date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('search_date')

        if not date:
            raise forms.ValidationError("Please correct the errors below.")
        if date > datetime.now().date():
            raise forms.ValidationError("Date must be today or  before "+str(datetime.now().date()))

        return cleaned_data


class ItemSearch(forms.Form):
    search_engine = forms.CharField(
        label='',
        max_length=1024,
        widget=forms.TextInput(attrs={'placeholder': 'Search...'}),
    )
    catalog = ChoiceField(
        label='',
        widget=forms.Select(),
        choices=[('name', 'name'), ('shelf', 'shelf position'), ('part_number', 'part number')],
        initial='name'
    )


class ItemMove(forms.Form):
    q = Q(quantity_in_store__gt=0)| Q(available_quantity__gt=0)
    all_items_in_store = Item.objects.filter(q).order_by('name')
    item_list = [(i.id, i) for i in all_items_in_store]
    item_list.insert(0, (None, '--------------'))
    item = ChoiceField(
        widget=forms.Select(),
        choices=item_list,
        required=True,
    )
    choose = ChoiceField(
        widget=forms.Select(),
        choices=[('from store', 'from store to shop'), ('to store', 'from shop to store')],
        required=True,
        label='select action'
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput,
        min_value=1,
        required=True,
    )
    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        choose = cleaned_data.get('choose')
        item_id = cleaned_data.get('item')
        if (not item_id) or (not quantity):
            raise forms.ValidationError("Please correct the errors below.")
        item  = Item.objects.get(pk=item_id)
        if choose == 'from store':
            if quantity > item.quantity_in_store:
                raise forms.ValidationError("only %s quantity in store for the selected item." % str(item.quantity_in_store))
        else:
            if quantity > item.available_quantity:
                raise forms.ValidationError("only %s quantity in shop for the selected item." % str(item.available_quantity))

        return cleaned_data
