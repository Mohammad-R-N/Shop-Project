from django.test import TestCase
from menu.models import Category, Product



class TestCategoryModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create( name = "category 1")

    def test_category_str(self):
        self.assertEquals(str(self.category), 'category 1')

class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create( name = "category 1")
        self.product = Product.objects.create( name = "product 1", price = 10.12 , category_menu = self.category, status = 'active')

    def test_category_str(self):
        self.assertEquals(str(self.product), 'product : product 1  price =10.12')