from django.test import TestCase
from cart.models import Cart, Table
from cart.admin import CartAdmin, TableAdmin
from decimal import Decimal
from django.contrib import admin

class CartAdminTest(TestCase):
    def test_accept_action(self):
        cart = Cart.objects.create(total_price=Decimal('0.00'),
            total_quantity=0,
            customer_number='+989123456789',
            cart_users=None,
            cart_table=Table.objects.create(table_name = 'test table'), status='Waiting')
        queryset = Cart.objects.filter(id=cart.id)
        cart_admin = CartAdmin(Cart, admin.site)
        cart_admin.accept(None, queryset)
        updated_cart = Cart.objects.get(id=cart.id)
        self.assertEqual(updated_cart.status, 'a')

