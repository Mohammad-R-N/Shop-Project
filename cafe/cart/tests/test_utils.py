from django.test import RequestFactory,TestCase
from cart.utils import ProductOption, Reservation, OrderDetail
from menu.models import Product,Category
from cart.models import *
from django.contrib.sessions.middleware import SessionMiddleware

class UtilsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.cat=Category.objects.create(name="drinks")
        self.product_model = Product.objects.create(name='cafe', photo='', price=10,description="hot drink",category_menu=self.cat)
    

    def test_showproduct(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        utils = ProductOption()
        cost, productlist = utils.show_product(request, self.product_model)
        self.assertEqual(cost, 0)
        self.assertEqual(len(productlist), 0)

    def test_remove_from_shop_cart(self):
        request = self.factory.post('/', {'remove': 'cafe'})
        utils = ProductOption()
        new_cookie = utils.remove_from_shop_cart(request)
        self.assertEqual(new_cookie, '')

    def test_accept_shop_cart(self):
        request = self.factory.post('/', {})
        request.COOKIES['product'] = 'cafe=1'
        utils = ProductOption()
        result = utils.accept_shop_cart(request)
        self.assertFalse(result)

    def test_checkout(self):
        self.table=Table.objects.create(table_name="table 1")
        request = self.factory.post('/', {'subject': self.table, 'tel': '09022631021'})
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session['cost'] = 10
        request.session['order'] = ['cafe=1']
        utils = Reservation()
        phone_number = utils.checkout(request, Product, Table, Cart, OrderItem)
        self.assertEqual(phone_number, '09022631021')

    def test_showcartdetail(self):
        request = self.factory.get('/')
        request.COOKIES['number'] = '09022631021'
        utils = OrderDetail()
        items, cart_list, status = utils.show_cart_detail(request, Cart, OrderItem)
        self.assertEqual(len(items), 0)
        self.assertEqual(len(cart_list), 0)
        self.assertEqual(len(status), 0)