from django.test import TestCase,RequestFactory
from users.models import CustomUser
from cart.models import Cart, OrderItem,Table
from menu.models import Category,Product
from customer.utils import CustomerOption

class CustomerOptionTestCase(TestCase):
    def setUp(self):
        self.customer_number = '09022631021'
        self.cat=Category.objects.create(name="drinks")
        self.pro=Product.objects.create(name="caffee",price=20,photo='',description ="dark drink",category_menu=self.cat)
        self.user = CustomUser.objects.create_user(phone_number="09123456789",password="Pa33Word")
        self.table=Table.objects.create(table_name="table 1")
        self.cart = Cart.objects.create(customer_number=self.customer_number,total_price=100,total_quantity =3,cart_users=self.user,cart_table =self.table)
        self.order_item1 = OrderItem.objects.create(cart=self.cart, quantity=2,price=20,product=self.pro)
        # self.order_item2 = OrderItem.objects.create(cart=self.cart, name='Item 2')

    def test_show_customer_history_with_matching_number(self):
        request = RequestFactory().get('/')
        request.COOKIES['number'] = self.customer_number

        item_list, cart_list = CustomerOption.show_customer_history(request, Cart, OrderItem)

        self.assertEqual(len(item_list), 1)
        self.assertEqual(len(cart_list), 1)
        self.assertEqual(item_list[0].product, self.pro)
        self.assertEqual(cart_list[0], self.cart)

    def test_show_customer_history_with_no_matching_number(self):
        request = RequestFactory().get('/')
        request.COOKIES['number'] = '54321'

        item_list, cart_list = CustomerOption.show_customer_history(request, Cart, OrderItem)

        self.assertEqual(len(item_list), 0)
        self.assertEqual(len(cart_list), 0)
