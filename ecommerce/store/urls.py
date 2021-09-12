import django
from django.urls import path
from . import views

from .views import (
    checkout,
)

urlpatterns = [
    path(r'', views.index, name='index'),
    path('checkout', views.checkout.as_view(), name='checkout'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('cart', views.cart, name='cart'),
    path('logout', views.logout, name='logout'),
    path('search_products', views.search_products, name='search_products'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart')
]

