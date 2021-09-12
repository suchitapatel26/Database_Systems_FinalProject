from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


# Create your models here.

class Product(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    url = models.TextField()
    description = models.TextField()
    list_price = models.FloatField()
    sale_price = models.FloatField()
    brand = models.TextField()
    stock_number = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def get_total_item_price(self):
        return self.quantity * self.product.sale_price


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.IntegerField()

    def __str__(self):
        return self.user.username
