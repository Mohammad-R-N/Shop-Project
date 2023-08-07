from django.contrib import admin
from . models import Product
from .models import Category
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_filter = ['status']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)