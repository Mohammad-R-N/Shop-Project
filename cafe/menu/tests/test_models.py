from django.test import TestCase
from menu.models import Category, Product


class TestCategoryModel(TestCase):
    def setUp(self):
         self.category = Category.objects.create( name = "category 1")

    def test_category_str(self):
        self.assertEquals(str(self.category), 'category 1')