from django.contrib import admin
from .models import Cart
from datetime import datetime, time
from .models import Product, OrderItem

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_customer', 'cart_users', 'time']

    list_editable = ['cart_users']


admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem)