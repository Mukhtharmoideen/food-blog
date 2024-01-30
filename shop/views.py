from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,InvalidPage


# Create your views here.
def home(request, c_slug=None):
    c_page = None
    product_list = None
    if c_slug != None:
        c_page = get_object_or_404(Categ, slug=c_slug)
        product_list = Product.objects.filter(category=c_page, available=True)
    else:
        product_list = Product.objects.all().filter(available=True)
    cat = Categ.objects.all()
    paginator = Paginator(product_list, 6)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page=1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products=paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'pr': product_list, 'ct': cat, "products": products})


def product_detail(request, c_slug, product_slug):
    try:
        prod = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'item.html', {'pr': prod})


# def searching(request):
#     prod = None
#     query = None
#     if 'q' in request.GET:
#         request.GET.get('q')
#         prod = Product.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
#
#     return render(request, 'search.html', {'qr': query, 'pr': prod})


def searching(request):
    prod = None
    query = request.GET.get('q')  # Retrieve the value from the GET parameter 'q'

    if query:  # Check if the query parameter is not None or an empty string
        prod = Product.objects.filter(Q(name__contains=query) | Q(desc__contains=query))
        # Using Q objects for searching in 'name' and 'desc' fields for the obtained query

    return render(request, 'search.html', {'qr': query, 'pr': prod})
