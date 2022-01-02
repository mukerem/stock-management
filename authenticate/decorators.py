from django.core.exceptions import PermissionDenied
from authenticate.models import User
from spare.models import Item, Supplier, Vehicle, StoreShelf, Sell, Purchase

def manager_auth(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_admin and request.user.role == 'manager':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def seller_auth(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'seller':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def manager_or_seller_auth(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_admin:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
    

def item_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            Item.objects.get(pk=kwargs['item_id'])
            return function(request, *args, **kwargs)
        except Item.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

    
def supplier_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            Supplier.objects.get(pk=kwargs['supplier_id'])
            return function(request, *args, **kwargs)
        except Supplier.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def vehicle_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            Vehicle.objects.get(pk=kwargs['vehicle_id'])
            return function(request, *args, **kwargs)
        except Vehicle.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def shelf_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            StoreShelf.objects.get(pk=kwargs['shelf_id'])
            return function(request, *args, **kwargs)
        except StoreShelf.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def sell_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            Sell.objects.get(pk=kwargs['sell_id'])
            return function(request, *args, **kwargs)
        except Sell.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def purchase_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            Purchase.objects.get(pk=kwargs['purchase_id'])
            return function(request, *args, **kwargs)
        except Purchase.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def seller_exist_validation(function):
    def wrap(request, *args, **kwargs):
        try:
            seller = User.objects.get(pk=kwargs['seller_id'])
            if seller.role == 'seller':
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        except User.DoesNotExist:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap