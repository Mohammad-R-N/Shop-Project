from django.test import TestCase,Client
from menu.models import Category, Product
from django.urls import reverse
from menu.models import Category, Product

class CategoryModelTest(TestCase):

    def setUp(self):
        self.client= Client()
        self.menu_url = reverse('menu')
        self.category = Category.objects.create( name = "category 1", photo = 'test.png')
        self.category2 = Category.objects.create( name = "category 2", photo = 'test.png')
        self.product = Product.objects.create( name = "product 1", price = 10.12 , category_menu = self.category, photo = 'product.png', status = 'active', )
        self.product2 = Product.objects.create( name = "product 2", price = 10.12 , category_menu = self.category, photo = 'product.png', status = 'active', )
        self.product3 = Product.objects.create( name = "product 3", price = 10.12 , category_menu = self.category2, photo = 'product.png', status = 'active', )

    def test_category_str(self):
        category = Category( name = "Test cat")
        self.assertEquals(str(category), "Test cat")  
        
    def test_name_label(self):
        category = Category.objects.get(id=self.category.id)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_photo_upload_to(self):
        category = Category.objects.get(id=self.category.id)
        upload_to = category._meta.get_field('photo').upload_to
        self.assertEqual(upload_to, 'media/category_photos')


class ProductModelTest(TestCase):

    def setUp(self):
        self.client= Client()
        self.menu_url = reverse('menu')
        self.category = Category.objects.create( name = "category 1", photo = 'test.png')
        self.category2 = Category.objects.create( name = "category 2", photo = 'test.png')
        self.product = Product.objects.create( name = "product 1", price = 10.12 , category_menu = self.category, photo = 'product.png', status = 'active', )
        self.product2 = Product.objects.create( name = "product 2", price = 10.12 , category_menu = self.category, photo = 'product.png', status = 'active', )
        self.product3 = Product.objects.create( name = "product 3", price = 10.12 , category_menu = self.category2, photo = 'product.png', status = 'active', )
        
    def test_name_label(self):
        product = Product.objects.get(id=self.product.id)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_price_max_digits(self):
        product = Product.objects.get(id=self.product.id)
        max_digits = product._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 6)

    def test_status_choices(self):
        product = Product.objects.get(id=self.product.id)
        status_choices = product._meta.get_field('status').choices
        self.assertEqual(status_choices, [('is_active', 'active'), ('not_active', 'inactive')])

    def test_photo_upload_to(self):
        product = Product.objects.get(id=self.product.id)
        upload_to = product._meta.get_field('photo').upload_to
        self.assertEqual(upload_to, 'media/menu_photos')

    def test_description_max_length(self):
        product = Product.objects.get(id=self.product.id)
        max_length = product._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)

    def test_point_default(self):
        product = Product.objects.get(id=self.product.id)
        default_point = product._meta.get_field('point').default
        self.assertEqual(default_point, 0)

    def test_category_menu_relation(self):
        product = Product.objects.get(id=self.product.id)
        related_model = product._meta.get_field('category_menu').related_model
        self.assertEqual(related_model, Category)