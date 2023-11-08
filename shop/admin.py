from django.contrib import admin
from .models import *


# Register your models here.


class Categ_dmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Categ, Categ_dmin)


class product_admin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'img']
    list_editable = ['price', 'stock', 'img']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, product_admin)
