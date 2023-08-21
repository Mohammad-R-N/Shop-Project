from django.test import TestCase
from menu.models import Product, Category
from menu.admin import ProductAdmin
from django.contrib import admin


class TestMenuAdmin(TestCase):

    def setUp(self):
        self.category = Category.objects.create( name = "category 1")
        self.product = Product.objects.create( name = "product 1", price = 10.00 , category_menu = self.category, status = 'active')

    def test_make_inactive_action(self):
         
        queryset = Product.objects.filter(id=self.product.id)
        product_admin = ProductAdmin(Product, admin.site)
        product_admin.make_inactive(None, queryset)
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.status, 'not_active')


