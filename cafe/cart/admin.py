from django.contrib import admin
from .models import Cart
from datetime import datetime, time
from .models import Product, OrderItem, Table

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_customer', 'cart_users', 'time']
    list_filter = ['time']
    list_editable = ['cart_users']


class TableAdmin(admin.ModelAdmin):
    list_display = ['table_name', 'table_seats', 'status']

admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem)
admin.site.register(Table, TableAdmin)

