from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import F

from .models import Product, Address, Order
from .forms import RegisterForm, CheckoutForm, CartAddProductForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from .cart import Cart
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', {"login_form": form})


def logout(request):
    auth_logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('/')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration Successful.")
            return redirect('/store')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm
    return render(request, 'register.html', {"form": form})


def index(request):
    products = Product.objects.raw('SELECT * FROM (SELECT * from store_product GROUP BY name)')
    paginator = Paginator(products, 100)
    page_number = request.GET.get('page')
    request.session['track_page'] = str(page_number)
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', context={'products': page_obj})


class checkout(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order_details = Order.objects.all()
        total = 0
        for order in order_details:
            order_product = Product.objects.get(id=order.product_id)
            total += order.get_total_item_price()

        context = {
            'form': form,
            'order_details': order_details,
            'total': total
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            if self.request.user.is_anonymous:
                messages.error(self.request, 'You must log-in to place an order.')
                return redirect('checkout')
            elif self.request.user != AnonymousUser and form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                address = Address(
                    user=self.request.user,
                    street_address=street_address,
                    country=country,
                    zip=zip,
                )
                address.save()
                messages.success(self.request, "Your order has been placed. Thank you for shopping with us.")
                return redirect('index')
            else:
                messages.error(self.request, "Invalid form. Please check the form and try again.")
                return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "Invalid form/You must log-in to place an order.")
            return redirect('checkout')



@require_POST
def add_to_cart(request):
    prod_id_val = request.POST.get('prod_id')
    prod = get_object_or_404(Product, id=prod_id_val)
    valid_user = request.user

    if str(valid_user) == "AnonymousUser":
        messages.info(request, "Please login to create your order!")
        return redirect('/store/login')
    else:
        hasProduct = Order.objects.filter(product=prod)
        if len(hasProduct) == 0:
            messages.info(request, "Product: " + str(prod) + " added to the cart!")
            add_product_to_cart = Order(user=User.objects.get(username=request.user),
                                        product=Product.objects.get(id=prod_id_val), quantity=1)
            add_product_to_cart.save()
        else:
            add_more = Order.objects.filter(product=prod).update(quantity=F('quantity') + 1)
            messages.info(request, "Product: " + str(prod) + " added one more quantity to the cart!")
        products = Product.objects.all()
        paginator = Paginator(products, 100)
        page_obj = paginator.get_page(request.session['track_page'])
        html = '/store/?page=' + request.session['track_page']
        return redirect(html, context={'products': page_obj})


def remove_from_cart(request):
    order_id = request.POST.get('order_id').split('/')[0]
    if order_id is not None or order_id != '':
        Order.objects.filter(id=int(order_id)).delete()
        messages.info(request, 'Product has been removed!')
        
    order_details = Order.objects.all()
    order_length = len(order_details)
    if order_length == 0:
        messages.info(request, "Your cart is empty!")
        return render(request, 'cart.html', {'order_length': order_length})
    else:
        total = 0
        for order in order_details:
            order_product = Product.objects.get(id=order.product_id)
            total += order.get_total_item_price()
        return render(request, 'cart.html', {'order_details': order_details,
                                             'products': order_product,
                                             'total': total})


def cart(request):
    order_details = Order.objects.all()
    order_length = len(order_details)
    if order_length == 0:
        messages.info(request, "Your cart is empty!")
        return render(request, 'cart.html', {'order_length': order_length})
    else:
        total = 0
        for order in order_details:
            order_product = Product.objects.get(id=order.product_id)
            total += order.get_total_item_price()
        return render(request, 'cart.html', {'order_details': order_details,
                                             'products': order_product,
                                             'total': total})



def search_products(request):
    if request.method == "POST":
        searched = request.POST.get('Search')
        print(searched)
        product = Product.objects.filter(name__contains=searched)
        return render(request,
                      'search_products.html',
                      {'searched': searched,
                       'products': product})
