from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Category, Product



class TestMenuView(TestCase):

    def setUp(self):
        self.client= Client()
        self.menu_url = reverse('menu')

    def test_menu_view_GET(self):
        response = self.client.get(self.menu_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu.html')


class TestSearchProducts(TestCase):
    def setUp(self):
        self.client= Client() 
        self.search_product_url = reverse('search_products')
