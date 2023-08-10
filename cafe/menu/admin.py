from django.contrib import admin
from . models import Product
from .models import Category
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ['name', 'price', 'category_menu']
    list_filter = ['status']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)