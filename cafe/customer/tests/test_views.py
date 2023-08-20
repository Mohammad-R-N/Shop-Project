from django.test import TestCase, Client
from django.urls import reverse
from cart.models import *


class TestCustomerView(TestCase):

    def setUp(self):
        self.client= Client()
        self.customer_url = reverse('customer-page')
        self.customer_history_url = reverse('customer-history')
   
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
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context)
        self.assertIn('carts', response.context)