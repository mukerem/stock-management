from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from authenticate.decorators import manager_auth, seller_auth, supplier_exist_validation, seller_exist_validation
from .models import User
from spare.models import Supplier
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import IntegrityError
import csv
from .forms import ChangePassword, EditMyProfile, SupplierRegister, EditSupplier, SellerRegister, EditSeller

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('stock_homepage')
    else:
        return redirect('login')

def check_role(request):
    if request.user.is_admin:
        return 'super_admin'
    elif request.user.role == 'manager':
        return 'manager'
    elif request.user.role == 'seller':
        return 'seller'

@login_required
def stock_homepage(request):
    role = check_role(request)
    if role == 'super_admin':
        return redirect('/admin/')
    elif role == 'manager':
        return redirect('manager_index')
    elif role == 'seller':
        return redirect('seller_index')


@login_required
@manager_auth
def manager_index(request):
    return render(request, 'manager_homepage.html')


@login_required
@seller_auth
def seller_index(request):
    return render(request, 'seller_homepage.html')


@login_required
def view_profile(request):
    user_role = request.user.role
    user_register_date = request.user.register_date
    initial_info = {'_role': user_role, '_register_date': user_register_date}
    if request.method == "POST":
        form = EditMyProfile(request.POST, request.FILES, instance=request.user, initial=initial_info)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "user "+post.username+" was update successfully.")
            return redirect('user_view_profile')
    else:
        form = EditMyProfile(instance=request.user, initial=initial_info)

    role = check_role(request)
    if role == 'manager':
        base_page = "manager_base_site.html"
    elif role == "seller":
        base_page = "seller_base_site.html"
    return render(request, 'profile.html', {'form': form, 'base_page': base_page})


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePassword(request.POST, password=request.user.password)
        if form.is_valid():
            new_password = request.POST.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "The password was changed successfully.")
    else:
        form = ChangePassword(password=request.user.password)
    role = check_role(request)
    if role == 'manager':
        base_page = "manager_base_site.html"
    elif role == "seller":
        base_page = "seller_base_site.html"
    return render(request, 'change_password.html', {'form': form,  'base_page': base_page})


@login_required
@manager_auth
def supplier_list(request):
	all_suppliers = Supplier.objects.all().order_by('name')
	return render(request, 'supplier_list.html', {'supplier_list': all_suppliers})


@login_required
@manager_auth
def supplier_register(request): 
	if request.method == "POST":
		form = SupplierRegister(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			messages.success(request, "Supplier %s was registered succesfully." % (post.name ))
			return redirect('supplier_register')          
	else:
		form = SupplierRegister()
	return render(request, 'supplier_register.html', {'form': form})



@login_required
@manager_auth
@supplier_exist_validation
def edit_supplier(request, supplier_id):
	supplier = Supplier.objects.get(id=supplier_id)
	if request.method == "POST":
		form = EditSupplier(request.POST, instance=supplier)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			messages.success(request, "supplier "+supplier.name+" was update successfully.")
			return redirect('edit_supplier', supplier_id)
	else:
		form = EditSupplier(instance=supplier)
	return render(request, 'edit_supplier.html', {'form': form})



@login_required
@manager_auth
@supplier_exist_validation
def delete_supplier(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    return render(request, 'delete_supplier.html', {'this_supplier': supplier})


@login_required
@manager_auth
@supplier_exist_validation
def delete_supplier_done(request, supplier_id):
    supplier = Supplier.objects.get(pk=supplier_id)
    supplier.delete()
    messages.success(request, "supplier  " + supplier.name + " was deleted successfully.")
    return redirect('supplier_list')


@login_required
@manager_auth
def seller_register(request):
    if request.method == "POST":
        form = SellerRegister(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.set_password(request.POST['user_password'])
            post.role = 'seller'
            post.save()
            messages.success(request, "user "+post.username+" was register successfully.")
            return redirect('seller_list')
    else:
        form = SellerRegister()
    return render(request, 'seller_register.html', {'form': form})


@login_required
@manager_auth
def seller_list(request):
	all_sellers = User.objects.filter(role = 'seller').order_by('username')
	return render(request, 'seller_list.html', {'seller_list': all_sellers})


@login_required
@manager_auth
@seller_exist_validation
def edit_seller(request, seller_id):
    seller = User.objects.get(pk=seller_id)
    if request.method == "POST":
        form = EditSeller(request.POST, request.FILES, instance=seller)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, "user "+post.username+" was update successfully.")
            redirect('edit_seller', seller_id)
    else:
        form = EditSeller(instance=seller)
    if seller.photo: photo = seller.photo.url
    else: photo=None
    return render(request, 'edit_seller.html', {'form': form, 'photo': photo})


@login_required
@manager_auth
@seller_exist_validation
def delete_seller(request, seller_id):
    seller = User.objects.get(pk=seller_id)
    return render(request, 'delete_seller.html', {'this_seller': seller})


@login_required
@manager_auth
@seller_exist_validation
def delete_seller_done(request, seller_id):
    seller = User.objects.get(pk=seller_id)
    seller.delete()
    messages.success(request, "seller  " + seller.username + " was deleted successfully.")
    return redirect('seller_list')

