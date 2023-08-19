from django.test import TestCase
from cart.models import *
from decimal import Decimal

class TestTableModel(TestCase):
    def setUp(self):
        self.table1 = Table.objects.create(table_name='Table 1', status='Available')

    def test_table_str(self):
        self.assertEquals(str(self.table1), 'Table: Table 1')

    def test_table_status_default(self):
        table2 = Table.objects.create(table_name= 'Table 2')
        self.assertEquals(table2.status, 'unavailable')

    def test_table_status(self):
        table2 = Table.objects.create(table_name= 'Table 2', status = 'Available')
        self.assertEquals(table2.status, 'Available')

    def test_table_update_status(self):
        self.table1.status = 'unavailable'
        self.table1.save()
        self.assertEqual(self.table1.status, 'unavailable')

    def test_table_status_max_length(self):
        max_length = Table._meta.get_field('status').max_length
        self.assertEqual(max_length, 20)

    def test_table_name_max_length(self):
        max_length = Table._meta.get_field('table_name').max_length
        self.assertEqual(max_length, 100)

    def test_table_status_choices(self):
        choices = [choice[0] for choice in Table.STATUS_CHOICES]
        self.assertListEqual(choices, ['Available', 'unavailable'])

    def test_table_each_status(self):
        self.assertEqual(Table.Available, 'Available')
        self.assertEqual(Table.unavailable, 'unavailable')

class TestCartModel(TestCase):
    def setUp(self):
        self.cart1 = Cart.objects.create(
            total_price=Decimal('0.00'),
            total_quantity=0,
            customer_number='+989123456789',
            cart_users=None,
            cart_table=Table.objects.create(table_name = 'test table'),
        )

    def test_cart_str(self):
        self.assertEquals(str(self.cart1), "0 order ")

    def test_cart_each_status(self):
        self.assertEqual(Cart.ACCEPT, 'a')
        self.assertEqual(Cart.REFUSE, 'r')
        self.assertEqual(Cart.WAITING, 'w')

    def test_cart_status_default(self):
        self.assertEquals(self.cart1.status, 'w')

    def test_cart_status_max_length(self):
        max_length = Cart._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

