from django.test import TestCase
from menu.models import Category, Product


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='TestCategory', photo='category_photo.jpg')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_photo_upload_to(self):
        category = Category.objects.get(id=1)
        upload_to = category._meta.get_field('photo').upload_to
        self.assertEqual(upload_to, 'media/category_photos')


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='TestCategory', photo='category_photo.jpg')
        Product.objects.create(name='TestProduct', price=10.00, status='is_active', photo='product_photo.jpg', description='Test description', point=5, category_menu=category)

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_price_max_digits(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field('price').max_digits
        self.assertEqual(max_digits, 6)

    def test_status_choices(self):
        product = Product.objects.get(id=1)
        status_choices = product._meta.get_field('status').choices
        self.assertEqual(status_choices, [('is_active', 'active'), ('not_active', 'inactive')])

    def test_photo_upload_to(self):
        product = Product.objects.get(id=1)
        upload_to = product._meta.get_field('photo').upload_to
        self.assertEqual(upload_to, 'media/menu_photos')

    def test_description_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('description').max_length
        self.assertEqual(max_length, 500)

    def test_point_default(self):
        product = Product.objects.get(id=1)
        default_point = product._meta.get_field('point').default
        self.assertEqual(default_point, 0)

    def test_category_menu_relation(self):
        product = Product.objects.get(id=1)
        related_model = product._meta.get_field('category_menu').related_model
        self.assertEqual(related_model, Category)