from django.test import TestCase
from menu.models import Product, Category
from menu.admin import ProductAdmin
from django.contrib import admin


class TestMenuAdmin(TestCase):

    def setUp(self):
        self.category = Category.objects.create( name = "category 1")
        self.product = Product.objects.create( name = "product 1", price = 10.00 , category_menu = self.category, status = 'active')



