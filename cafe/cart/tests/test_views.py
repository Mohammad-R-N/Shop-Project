from django.test import TestCase, Client
from django.urls import reverse
from cart.models import *
from menu.models import Category
from decimal import Decimal
from django.contrib.messages import get_messages
from django.contrib.messages import constants as messages
from cart.utils import ProductOption
from cart.views import CartView
from unittest.mock import patch


class TestCartView(TestCase):

    def setUp(self):
        self.client= Client()
        self.cart_url = reverse('cart')
        self.category = Category.objects.create(name = 'food')
        self.product = Product.objects.create(name='Pizza', price=10.00, category_menu = self.category)
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
        self.assertTrue('product' in self.client.cookies)
        self.assertEqual(self.client.cookies['product'].value, 'Pizza')
        self.assertEqual(str(self.product), 'product : Pizza  price =10.0')
        

    def test_post_remove(self):
        with patch.object(ProductOption, 'remove_from_shop_cart') as mock_remove:
            response = self.client.post(self.cart_url, {"remove": "true"})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('cart'))
            
            self.assertTrue(mock_remove.called)

    def test_post_done(self):
        with patch.object(ProductOption, 'accept_shop_cart') as mock_remove:
            response = self.client.post(self.cart_url, {"done": "true"})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('reservation'))
            
            self.assertTrue(mock_remove.called)

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

    def test_ord_deatil_view_GET_context_without_cookie(self):
        response = self.client.get(self.ord_detail_url)

        self.assertNotIn('cart', response.context)
        self.assertNotIn('items', response.context)
        self.assertNotIn('process', response.context)

    def test_ord_deatil_view_GET_context_with_cookie(self):
        self.client.cookies['number'] = '09123456789'
        response = self.client.get(self.ord_detail_url)

        self.assertIn('cart', response.context)
        self.assertIn('items', response.context)
        self.assertIn('process', response.context)

    def test_ord_detail_message(self):
        self.client.cookies['number'] = '09123456789'
        response = self.client.get(self.ord_detail_url)

        my_message = get_messages(response.wsgi_request)
        self.assertEqual(len(my_message), 1)
        message = list(my_message)[0]
        self.assertEqual(message.level, messages.SUCCESS)
        self.assertEqual(message.message, 'Your ORDER has send successfully!')


class TestReservationView(TestCase):
    
    def setUp(self):
        self.client= Client()
        self.ord_detail_url = reverse('reservation')


