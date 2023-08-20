from django.test import TestCase, Client
from django.urls import reverse
from cart.models import *


class TestCustomerView(TestCase):

    def setUp(self):
        self.client= Client()
        self.customer_url = reverse('customer-page')

