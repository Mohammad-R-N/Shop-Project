from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Category, Product



class TestMenuView(TestCase):

    def setUp(self):
        self.client= Client()
        self.menu_url = reverse('menu')
        self.search_product_url = reverse('search_products')


