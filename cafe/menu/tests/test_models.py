from django.test import TestCase
from menu.models import Category, Product


class TestCategoryModel(TestCase):
    def setUp(self):
         self.category = Category.objects.create( name = "category 1")
