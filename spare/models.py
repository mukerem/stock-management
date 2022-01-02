from django.utils.safestring import mark_safe
from django.core.exceptions  import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from authenticate.models import User
# Create your models here.


class Vehicle(models.Model):
	name = models.CharField(max_length=200, unique=True)
	discription = models.CharField(max_length=400, blank=True)

	def __str__(self):
		return self.name


class StoreShelf(models.Model):
	name = models.CharField(max_length=200, unique=True)
	place = models.CharField(max_length=400, blank=True)

	def __str__(self):
		return self.name

class Supplier(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=500, blank=True)
	phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 09******** or +2519******** up to 15 digits allowed',
    )
	phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
	loan = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)

	def __str__(self):
		return self.name

class Item(models.Model):
	part_number = models.CharField(max_length=200, unique=True)
	name = models.CharField(max_length=200, unique=True)
	purchase_price  = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
	selling_price  = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
	available_quantity = models.PositiveIntegerField(default=0)
	quantity_in_store = models.PositiveIntegerField(default=0)
	measurment = models.CharField(max_length=200, choices=(('piece', 'piece'), ('set', 'set')))
	type_of_car = models.ManyToManyField(Vehicle, blank=True)
	purchase_date = models.DateField(default = now)
	shelf = models.ManyToManyField(StoreShelf)
	photo = models.ImageField(blank=True, upload_to='')

	def __str__(self):
		return "%s(%s)" % (self.name, self.part_number)

	def image_tag(self):
		return mark_safe('<img src="%s", width="150", height="150"/>' % self.photo.url)
	
	image_tag.short_description = 'Photo'
	image_tag.allow_tags = True


class Sell(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])	
	selling_price  = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField(default=now)
	vat = models.BooleanField(default=False)

	def __str__(self):
		return "%s by %s" % (self.item, self.seller)

	def update_quantity(self):
		post = self.item
		post.available_quantity -= self.quantity
		post.save()


class Purchase(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'manager'})
	purchase_price  = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
	selling_price  = models.DecimalField(decimal_places=2, max_digits=20, default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
	supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
	date = models.DateField(default=now)

	def __str__(self):
		return "%s by %s from %s" % (self.item, self.buyer, self.supplier)

	def update_quantity(self):
		post = self.item
		post.available_quantity += self.quantity
		post.save()