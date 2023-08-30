from django.test import TestCase, Client
from django.urls import reverse
from cart.models import *
import json
from menu.models import Category
from decimal import Decimal


class TestCartView(TestCase):

    def setUp(self):
        self.client= Client()
        self.cart_url = reverse('cart')
        self.category = Category.objects.create(name = 'food')
        self.product = Product.objects.create(name='Pizza', price=Decimal('10.00'), category_menu = self.category)
        self.cart = Cart.objects.create(total_price=Decimal('0.00'), total_quantity=0,  customer_number = "09191234567", cart_table=Table.objects.create(table_name = "test table"),)
    
   
    def test_cart_view_GET(self):
        response = self.client.get(self.cart_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        

    def test_cart_view_GET_with_cookie(self):
        self.client.cookies['product'] = 'Pizza'
        response = self.client.get(self.cart_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html') 



class TestOrdDetailView(TestCase):

    def setUp(self):
        self.client= Client()
        self.ord_detail_url = reverse('ord_detail')

    def test_ord_deatil_view_GET(self):
        response = self.client.get(self.ord_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_ord_detail.html')

    def test_ord_deatil_view_GET_with_cookie(self):
        self.client.cookies['number'] = '09123456789'
        response = self.client.get(self.ord_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer/customer_ord_detail.html')