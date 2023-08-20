from django.test import TestCase, Client
from django.urls import reverse
from cart.models import *
from menu.models import Category
from decimal import Decimal


class TestCustomerView(TestCase):

    def setUp(self):
        self.client= Client()
        self.customer_url = reverse('customer-page')
        self.customer_history_url = reverse('customer-history')

        self.table1 = Table.objects.create(table_name = 'table 1')
        self.table2 = Table.objects.create(table_name = 'table 2')
        self.cart1 = Cart.objects.create(customer_number='09123456789', total_price = Decimal("10.00") , total_quantity = 2, cart_table = self.table1, )
        self.cart2 = Cart.objects.create(customer_number='09191234567', total_price = Decimal("30.00") , total_quantity = 3, cart_table = self.table2, )
        
        self.category1 = Category.objects.create(name = 'food')
        self.category2 = Category.objects.create(name = 'drinks')
        self.item1 = OrderItem.objects.create(product=Product.objects.create(name = 'pizza', price = Decimal('5.00'), category_menu = self.category1),
            cart = self.cart1,
            quantity = 2,
            price = Decimal('10.00'))
        
        self.item2 = OrderItem.objects.create(product=Product.objects.create(name = 'mocha', price = Decimal('10.00'), category_menu = self.category2),
            cart = self.cart2,
            quantity = 3,
            price = Decimal('30.00'))
   
    def test_customer_view_GET(self):
        response = self.client.get(self.customer_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer.html')

    def test_customer_hostory_GET(self):
        response = self.client.get(self.customer_history_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/history.html')

    def test_get_with_cookies(self):
        self.client.cookies['number'] = '12345'
        response = self.client.get(self.customer_history_url)
        self.assertIn('items', response.context)
        self.assertIn('carts', response.context)

    def test_get_without_cookies(self):
        response = self.client.get(self.customer_history_url)
        self.assertNotIn('items', response.context)
        self.assertNotIn('carts', response.context)

    def test_get_filter_items_and_carts(self):
        self.client.cookies['number'] = '09123456789'
        response = self.client.get(self.customer_history_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(len(response.context['carts']), 1)
        self.assertEqual(response.context['items'][0], self.item1)
        self.assertEqual(response.context['carts'][0], self.cart1)