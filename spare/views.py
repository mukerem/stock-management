from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from authenticate.decorators import manager_auth, seller_auth, manager_or_seller_auth, item_exist_validation,\
	shelf_exist_validation, vehicle_exist_validation, sell_exist_validation, purchase_exist_validation
from .models import Item, Sell, Purchase, StoreShelf, Vehicle
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.db import IntegrityError
import csv
import datetime
from authenticate.views import check_role
from .forms import EditItem, ItemRegister, NewSell, NewPurchase, EditShelf, ShelfRegister, EditVehicle,\
	 VehicleRegister, EditSell, EditPurchase, DateSearchEngine, ItemSearch, ItemMove
import math
@login_required
@seller_auth
def product_list(request):
	all_products = Item.objects.all().only('part_number', 'name', 'selling_price', 'available_quantity', 'type_of_car', 'shelf').order_by('name')
	for i in all_products:
		cars = ', '.join([ str(j.name) for j in i.type_of_car.all()])
		i.car_type = cars
		shelf = ', '.join([ str(j.name) for j in i.shelf.all()])
		i.shelf_position = shelf
	return render(request, 'product_list.html', {'product_list': all_products})


@login_required
@manager_auth
def item_register(request): 
	if request.method == "POST":
		form = ItemRegister(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.available_quantity = post.quantity
			post.save()
			form.save_m2m() 
			messages.success(request, "item " + post.name + " was register successfully.")
			return redirect('stock_item')          
	else:
		form = ItemRegister()
	return render(request, 'item_register.html', {'form': form})


@login_required
@manager_auth
def stock_item(request):
	all_items = Item.objects.all().order_by('name')
	for i in all_items:
		cars = ', '.join([ str(j.name) for j in i.type_of_car.all()])
		i.car_type = cars
		shelf = ', '.join([ str(j.name) for j in i.shelf.all()])
		i.shelf_position = shelf
	return render(request, 'stock_item.html', {'item_list': all_items})


@login_required
@manager_auth
def store_item_list(request):
	all_items = Item.objects.filter(quantity_in_store__gt=0).order_by('name')
	for i in all_items:
		cars = ', '.join([ str(j.name) for j in i.type_of_car.all()])
		i.car_type = cars
	return render(request, 'store_item_list.html', {'item_list': all_items})


@login_required
@manager_auth
@item_exist_validation
def edit_item(request, item_id):
	item = Item.objects.get(id=item_id)
	if request.method == "POST":
		form = EditItem(request.POST, request.FILES, instance=item)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			form.save_m2m()
			messages.success(request, "item "+item.name+" was update successfully.")
			return redirect('edit_item', item_id)
	else:
		form = EditItem(instance=item)
	if item.photo: photo = item.photo.url
	else: photo=None
	return render(request, 'edit_item.html', {'form': form, 'photo': photo})



@login_required
@manager_auth
@item_exist_validation
def delete_item(request, item_id):
    item = Item.objects.get(pk=item_id)
    return render(request, 'delete_item.html', {'this_item': item})


@login_required
@manager_auth
@item_exist_validation
def delete_item_done(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.delete()
    messages.success(request, "item  " + item.name + " was deleted successfully.")
    return redirect('stock_item')


@login_required
@manager_or_seller_auth
def new_sell(request): 
	if request.method == "POST":
		form = NewSell(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.seller = request.user
			post.save()
			form.save_m2m() 
			Sell.update_quantity(post)
			messages.success(request, "item %s was sell %s quantity." % (post.item.name , str(post.quantity)))
			return redirect('item_sell_list', 'Today')          
	else:
		form = NewSell()
	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'new_sell.html', {'form': form, 'base_page': base_page})


@login_required
@manager_or_seller_auth
def ajax_update_sell_data(request):
    item_id = request.GET.get('item')
    item = Item.objects.get(pk=item_id)
    response_data = {'selling_price': item.selling_price}
    return JsonResponse(response_data , content_type="application/json")


@login_required
@manager_auth
def ajax_update_purchase_data(request):
    item_id = request.GET.get('item')
    item = Item.objects.get(pk=item_id)
    response_data = {'selling_price': item.selling_price, 'purchase_price': item.purchase_price}
    return JsonResponse(response_data , content_type="application/json")


@login_required
@manager_or_seller_auth
def item_sell_list(request, date): 
	if date == 'Today':
		all_sell = Sell.objects.filter(date = now())
	elif date == 'Yesterday':
		yesterday = now() - datetime.timedelta(days=1)
		all_sell = Sell.objects.filter(date = yesterday)
	elif date == 'This Week':
		this_week = now() - datetime.timedelta(days=7)
		all_sell = Sell.objects.filter(date__gte = this_week).order_by('date').reverse()		
	elif date == 'This Month':
		all_sell = Sell.objects.filter(date__month = now().month).order_by('date').reverse()
	elif date == 'This Year':
		all_sell = Sell.objects.filter(date__year = now().year).order_by('date').reverse()

	total_cost = 0.00
	for i in all_sell:
		single_item_price = i.quantity * float(i.selling_price)
		i.total_price = single_item_price
		total_cost += single_item_price

	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'item_sell_list.html', {'sell_list': all_sell, 'total_cost':total_cost, 'date': date, 'base_page': base_page})



@login_required
@manager_auth
def vat_sell_list(request, date): 
	if date == 'Today':
		all_sell = Sell.objects.filter(date = now(), vat=True)
	elif date == 'Yesterday':
		yesterday = now() - datetime.timedelta(days=1)
		all_sell = Sell.objects.filter(date = yesterday, vat=True)
	elif date == 'This Week':
		this_week = now() - datetime.timedelta(days=7)
		all_sell = Sell.objects.filter(date__gte = this_week, vat=True).order_by('date').reverse()		
	elif date == 'This Month':
		all_sell = Sell.objects.filter(date__month = now().month, vat=True).order_by('date').reverse()
	elif date == 'This Year':
		all_sell = Sell.objects.filter(date__year = now().year, vat=True).order_by('date').reverse()

	total_cost = 0.00
	total_vat = 0.00
	total_cost_with_vat = 0.00
	for i in all_sell:
		single_item_price = i.quantity * float(i.selling_price)
		single_item_vat = round(single_item_price * 0.15, 2)
		single_item_price_with_vat = round(single_item_price * 1.15, 2)
		i.total_price = single_item_price
		i.vat_price = single_item_vat
		i.total_price_with_vat = single_item_price_with_vat
		total_cost += single_item_price
		total_vat += single_item_vat
		total_cost_with_vat += single_item_price_with_vat
	return render(request, 'vat_sell_list.html', {'sell_list': all_sell, 'total_cost':total_cost, 'total_vat': total_vat, 'total_cost_with_vat': total_cost_with_vat,  'date': date})


@login_required
@manager_or_seller_auth
@item_exist_validation
def select_item_to_sell(request, item_id): 
	item = Item.objects.get(pk=item_id)
	initial_info = {'item': item, 'selling_price': item.selling_price}
	if request.method == "POST":
		form = NewSell(request.POST, initial=initial_info)
		if form.is_valid():
			post = form.save(commit=False)
			post.seller = request.user
			post.save()
			form.save_m2m() 
			Sell.update_quantity(post)
			messages.success(request, "item %s was sell %s quantity." % (post.item.name , str(post.quantity)))
			return redirect('item_sell_list', 'Today')          
	else:
		form = NewSell(initial=initial_info)
	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'new_sell.html', {'form': form, 'base_page': base_page})


@login_required
@manager_auth
def sell_search_by_date(request):
	all_sell = Sell.objects.filter(date=now())
	date = 'today'
	if request.method == "POST":
		form = DateSearchEngine(request.POST)
		if form.is_valid():
			date = request.POST.get('search_date')
			all_sell = Sell.objects.filter(date = date)
	else:
		form = DateSearchEngine()

	total_cost = 0.00
	for i in all_sell:
		single_item_price = i.quantity * float(i.selling_price)
		i.total_price = single_item_price
		total_cost += single_item_price
	return render(request, 'item_sell_search_by_date.html', {'form': form, 'sell_list': all_sell, 'total_cost':total_cost, 'date': date})



@login_required
@manager_auth
def purchase_search_by_date(request):
	all_purchase = Purchase.objects.filter(date=now())
	date = 'today'
	if request.method == "POST":
		form = DateSearchEngine(request.POST)
		if form.is_valid():
			date = request.POST.get('search_date')
			all_purchase = Purchase.objects.filter(date = date)
	else:
		form = DateSearchEngine()

	total_cost = 0.00
	for i in all_purchase:
		single_item_price = i.quantity * float(i.purchase_price)
		i.total_price = single_item_price
		total_cost += single_item_price
	return render(request, 'item_purchase_search_by_date .html', {'form': form, 'purchase_list': all_purchase, 'total_cost':total_cost, 'date': date})



@login_required
@manager_or_seller_auth
@sell_exist_validation
def edit_sell(request, sell_id): 
	sell = Sell.objects.get(pk=sell_id)
	prevous_quantity = sell.quantity
	item = sell.item
	if request.method == "POST":
		form = EditSell(request.POST, instance=sell)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			form.save_m2m()
			item.available_quantity += (prevous_quantity - post.quantity)
			item.save()
			# Sell.update_quantity(post)
			messages.success(request, "sell of item %s was update successfully" % (post.item.name))
			return redirect('item_sell_list', 'Today')          
	else:
		form = EditSell(instance=sell)
	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'edit_sell.html', {'form': form, 'base_page': base_page})


@login_required
@manager_or_seller_auth
@sell_exist_validation
def delete_sell(request, sell_id):
	sell = Sell.objects.get(pk=sell_id)
	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'delete_sell.html', {'this_sell': sell, 'base_page': base_page})


@login_required
@manager_or_seller_auth
@sell_exist_validation
def delete_sell_done(request, sell_id):
    sell = Sell.objects.get(pk=sell_id)
    sell.delete()
    messages.success(request, "sell of item " + sell.item.name + " was deleted successfully.")
    return redirect('item_sell_list', 'Today')


@login_required
@manager_auth
def new_purchase(request): 
	if request.method == "POST":
		form = NewPurchase(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			stock_quantity = int(request.POST.get('stock_quantity'))
			store_quantity = int(request.POST.get('store_quantity'))
			post.buyer = request.user
			post.save()
			form.save_m2m() 
			item = post.item
			item.selling_price = post.selling_price
			item.purchase_price = post.purchase_price
			item.quantity_in_store += store_quantity
			item.available_quantity += stock_quantity
			item.save()
			# Purchase.update_quantity(post)
			messages.success(request, "item %s was purchase %s quantity." % (post.item.name , str(post.quantity)))
			return redirect('item_purchase_list', 'Today')          
	else:
		form = NewPurchase()
	return render(request, 'new_purchase.html', {'form': form})


@login_required
@manager_auth
def item_purchase_list(request, date): 
	if date == 'Today':
		all_purchase = Purchase.objects.filter(date = now()).order_by('date').reverse()
	elif date == 'Yesterday':
		yesterday = now() - datetime.timedelta(days=1)
		all_purchase = Purchase.objects.filter(date = yesterday).order_by('date').reverse()
	elif date == 'This Week':
		this_week = now() - datetime.timedelta(days=7)
		all_purchase = Purchase.objects.filter(date__gte = this_week).order_by('date').reverse()
	elif date == 'This Month':
		all_purchase = Purchase.objects.filter(date__month = now().month).order_by('date').reverse()
	elif date == 'This Year':
		all_purchase = Purchase.objects.filter(date__year = now().year).order_by('date').reverse()

	total_cost = 0.00
	for i in all_purchase:
		single_item_price = i.quantity * float(i.purchase_price)
		i.total_price = single_item_price
		total_cost += single_item_price
	return render(request, 'item_purchase_list.html', {'purchase_list': all_purchase, 'total_cost':total_cost, 'date': date})


@login_required
@manager_auth
@purchase_exist_validation
def edit_purchase(request, purchase_id): 
	purchase = Purchase.objects.get(pk=purchase_id)
	prevous_quantity = purchase.quantity
	item = purchase.item
	if request.method == "POST":
		form = EditPurchase(request.POST, instance=purchase)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			form.save_m2m()
			stock_quantity = int(request.POST.get('stock_quantity'))
			store_quantity = int(request.POST.get('store_quantity'))
			item.available_quantity += (stock_quantity - prevous_quantity )
			item.quantity_in_store += (store_quantity - prevous_quantity )
			item.save()
			# Sell.update_quantity(post)
			messages.success(request, "purchase of item %s was update successfully" % (post.item.name))
			return redirect('item_purchase_list', 'Today')          
	else:
		form = EditPurchase(instance=purchase)
	return render(request, 'edit_purchase.html', {'form': form})


@login_required
@manager_auth
@purchase_exist_validation
def delete_purchase(request, purchase_id):
	purchase = Purchase.objects.get(pk=purchase_id)
	return render(request, 'delete_purchase.html', {'this_purchase': purchase})


@login_required
@manager_auth
@purchase_exist_validation
def delete_purchase_done(request, purchase_id):
    purchase = Purchase.objects.get(pk=purchase_id)
    purchase.delete()
    messages.success(request, "purchase of item " + purchase.item.name + " was deleted successfully.")
    return redirect('item_purchase_list', 'Today')

	
@login_required
@manager_auth
def shelf_register(request): 
	if request.method == "POST":
		form = ShelfRegister(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			messages.success(request, "shelf " + post.name + " was register successfully.")
			return redirect('shelf_list')          
	else:
		form = ShelfRegister()
	return render(request, 'shelf_register.html', {'form': form})


@login_required
@manager_auth
def shelf_list(request):
	all_shelfs = StoreShelf.objects.all().order_by('name')
	return render(request, 'shelf_list.html', {'shelf_list': all_shelfs})


@login_required
@manager_auth
@shelf_exist_validation
def edit_shelf(request, shelf_id):
	shelf = StoreShelf.objects.get(id=shelf_id)
	if request.method == "POST":
		form = EditShelf(request.POST, instance=shelf)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			messages.success(request, "shelf "+shelf.name+" was update successfully.")
			return redirect('edit_shelf', shelf_id)
	else:
		form = EditShelf(instance=shelf)
	return render(request, 'edit_shelf.html', {'form': form})



@login_required
@manager_auth
@shelf_exist_validation
def delete_shelf(request, shelf_id):
    shelf = StoreShelf.objects.get(pk=shelf_id)
    return render(request, 'delete_shelf.html', {'this_shelf': shelf})


@login_required
@manager_auth
@shelf_exist_validation
def delete_shelf_done(request, shelf_id):
    shelf = StoreShelf.objects.get(pk=shelf_id)
    shelf.delete()
    messages.success(request, "shelf  " + shelf.name + " was deleted successfully.")
    return redirect('shelf_list')


@login_required
@manager_auth
def vehicle_register(request): 
	if request.method == "POST":
		form = VehicleRegister(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			messages.success(request, "vehicle " + post.name + " was register successfully.")
			return redirect('vehicle_list')          
	else:
		form = VehicleRegister()
	return render(request, 'vehicle_register.html', {'form': form})


@login_required
@manager_auth
def vehicle_list(request):
	all_vehicles = Vehicle.objects.all().order_by('name')
	return render(request, 'vehicle_list.html', {'vehicle_list': all_vehicles})


@login_required
@manager_auth
@vehicle_exist_validation
def edit_vehicle(request, vehicle_id):
	vehicle = Vehicle.objects.get(id=vehicle_id)
	if request.method == "POST":
		form = EditVehicle(request.POST, instance=vehicle)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			messages.success(request, "vehicle "+vehicle.name+" was update successfully.")
			return redirect('edit_vehicle', vehicle_id)
	else:
		form = EditVehicle(instance=vehicle)
	return render(request, 'edit_vehicle.html', {'form': form})



@login_required
@manager_auth
@vehicle_exist_validation
def delete_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    return render(request, 'delete_vehicle.html', {'this_vehicle': vehicle})


@login_required
@manager_auth
@vehicle_exist_validation
def delete_vehicle_done(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    vehicle.delete()
    messages.success(request, "vehicle  " + vehicle.name + " was deleted successfully.")
    return redirect('vehicle_list')


@login_required
@manager_auth
def capital(request):
	all_items = Item.objects.all()
	purchase_capital = 0.00
	selling_capital = 0.00
	for i in all_items:
		current_quantity = i.available_quantity + i.quantity_in_store
		single_item_purchase_cost = current_quantity * float(i.purchase_price)
		single_item_selling_cost = current_quantity * float(i.selling_price)
		i.total_purchase_cost = single_item_purchase_cost
		i.total_selling_cost = single_item_selling_cost
		i.current_quantity = current_quantity
		purchase_capital += single_item_purchase_cost
		selling_capital += single_item_selling_cost
	return render(request, 'capital.html', {'all_items': all_items, 'purchase_capital':purchase_capital, 'selling_capital':selling_capital})


@login_required
@manager_or_seller_auth
def search_item(request):
	if request.method == "POST":
		form = ItemSearch(request.POST)
		text = request.POST.get('search_engine')
		catalog = request.POST.get('catalog')
		if catalog == 'name':
			all_items = Item.objects.filter(name__contains=text).order_by('name')
		elif catalog == 'shelf':
			all_items = Item.objects.filter(shelf__name__contains=text).order_by('name')
		elif catalog == 'part_number':
			all_items = Item.objects.filter(part_number__contains=text).order_by('name')
	else:
		form = ItemSearch()
		all_items = Item.objects.all().order_by('name')
	for i in all_items:
		cars = ', '.join([ str(j.name) for j in i.type_of_car.all()])
		i.car_type = cars
		shelf = ', '.join([ str(j.name) for j in i.shelf.all()])
		i.shelf_position = shelf

	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'item_search.html', {'form':form, 'item_list': all_items, 'base_page': base_page})



@login_required
@manager_or_seller_auth
def empty_item(request):
	all_items = Item.objects.filter(available_quantity=0).order_by('name')
	for i in all_items:
		cars = ', '.join([ str(j.name) for j in i.type_of_car.all()])
		i.car_type = cars
		shelf = ', '.join([ str(j.name) for j in i.shelf.all()])
		i.shelf_position = shelf
	role = check_role(request)
	if role == 'manager':
		base_page = "manager_base_site.html"
	elif role == "seller":
		base_page = "seller_base_site.html"
	return render(request, 'empty_item.html', {'item_list': all_items, 'base_page': base_page})


@login_required
@manager_auth
def store_item_move(request):
	if request.method == "POST":
		form = ItemMove(request.POST)
		if form.is_valid():
			item_id = request.POST.get('item')
			choose = request.POST.get('choose')
			quantity = int(request.POST.get('quantity'))
			item  = Item.objects.get(pk=item_id)
			if choose == 'from store':
				item.available_quantity += quantity
				item.quantity_in_store -= quantity
			else:
				item.available_quantity -= quantity
				item.quantity_in_store += quantity
			item.save()
			messages.success(request, "item %s was move %s %s quantity successfully." %(item.name, choose , str(quantity)))
			return redirect('store_item_move')
	else:
		form = ItemMove()
	return render(request, 'item_move.html', {'form': form})
