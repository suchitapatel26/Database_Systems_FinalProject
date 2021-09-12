from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product, Order, Address

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Address)
