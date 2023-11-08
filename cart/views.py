from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from shop.models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def cartDetails(request, tot=0, count=0, cart_items=None):
    try:
        ct = CartList.objects.get(cart_id=c_id(request))
        ct_items = Items.objects.filter(cart=ct, active=True)
        for i in ct_items:
            tot += (i.prodt.price * i.quan)
            count += i.quan
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', {'ci': ct_items, 't': tot, 'cn': count})


def c_id(request):
    ct_id = request.session.session_key
    if not ct_id:
        ct_id = request.session.create()
    return ct_id


def add_cart(request, product_id):
    prod = Product.objects.get(id=product_id)
    cart_id = c_id(request)

    try:
        cart = CartList.objects.get(cart_id=cart_id)
    except CartList.DoesNotExist:
        cart = CartList.objects.create(cart_id=cart_id)

    try:
        cart_item = Items.objects.get(prodt=prod, cart=cart)
        if cart_item.quan < prod.stock:
            cart_item.quan += 1
            cart_item.save()
    except Items.DoesNotExist:
        if prod.stock > 0:
            Items.objects.create(prodt=prod, quan=1, cart=cart)

    return redirect('cartDetails')


def min_cart(request, product_id):
    ct = CartList.objects.get(cart_id=c_id(request))
    prod = get_object_or_404(Product,id=product_id)
    c_items = Items.objects.get(prodt=prod, cart=ct)
    if c_items.quan > 1:
        c_items.quan -= 1
        c_items.save()
    else:
        c_items.delete()
    return redirect('cartDetails')

def cart_delete(request,product_id):
    ct = CartList.objects.get(cart_id=c_id(request))
    prod = get_object_or_404(Product, id=product_id)
    c_items = Items.objects.get(prodt=prod, cart=ct)
    c_items.delete()
    return redirect('cartDetails')
