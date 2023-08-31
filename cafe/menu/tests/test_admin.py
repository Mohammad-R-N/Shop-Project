from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from menu.admin import ProductAdmin, CategoryAdmin
from menu.models import Category, Product
from users.models import CustomUser
class ProductAdminTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_superuser(
            phone_number = '09123456789',
            password='admin'
        )

    def test_make_inactive_action(self):
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            name='Test Product',
            price=10.0,
            category_menu=category,
            status='active'
        )
        product_admin = ProductAdmin(Product, AdminSite())
        request = self.factory.post('/admin/myapp/product/', {'action': 'make_inactive', '_selected_action': [product.id]})
        request.user = self.user

        queryset = Product.objects.filter(id__in=[product.id])
        product_admin.make_inactive(request, queryset)

        product = Product.objects.get(id=product.id)
        self.assertEqual(product.status, 'not_active')

class CategoryAdminTest(TestCase):
    def test_search_fields(self):
        category_admin = CategoryAdmin(Category, AdminSite())
        self.assertEqual(category_admin.search_fields, ['name'])

    def test_list_display(self):
        category_admin = CategoryAdmin(Category, AdminSite())
        self.assertEqual(category_admin.list_display, ['name'])