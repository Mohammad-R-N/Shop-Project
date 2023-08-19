from django.test import TestCase, Client
from django.urls import reverse
from cart.models import *
import json

class TestCartView(TestCase):
    def test_cart_view_GET(self):
        client= Client()
        response = client.get(reverse('cart'))

        self.assertEquals(response.status_code, 200)