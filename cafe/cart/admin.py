from django.contrib import admin
from .models import Cart
from datetime import datetime, time
from .models import OrderItem, Table

class CartAdmin(admin.ModelAdmin):

    actions = ['accept']
    @admin.action(description='Mark Selected Carts to Accept')
    def accept(self, request, queryset):
        queryset.update(status='a')

    list_display = ['customer_number', 'cart_users', 'time']
    list_filter = ['time']
    list_editable = ['cart_users']


class TableAdmin(admin.ModelAdmin):
    list_display = ['table_name', 'status']

admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem)
admin.site.register(Table, TableAdmin)

