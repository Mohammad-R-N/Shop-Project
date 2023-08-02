from django.contrib import admin
from .models import Cart
from datetime import datetime, time

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_customer', 'cart_staff', 'time']

    list_editable = ['cart_staff']


admin.site.register(Cart, CartAdmin)