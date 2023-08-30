from django.test import TestCase
from cart.models import OrderItem, Cart, Table
from users.models import CustomUser
from datetime import datetime
from django.http import HttpRequest
from django.contrib.messages.storage.fallback import FallbackStorage
from menu.models import *
from users.utils import *

class TestUtils(TestCase):
    def setUp(self):
        self.customer_number = '09022631021'
        self.cat=Category.objects.create(name="drinks")
        self.pro=Product.objects.create(name="caffee",price=20,photo='',description ="dark drink",category_menu=self.cat)
        self.user = CustomUser.objects.create_user(phone_number="09123456789",password="Pa33Word")
        self.table=Table.objects.create(table_name="table 1")
        self.cart = Cart.objects.create(customer_number=self.customer_number,total_price=100,total_quantity =3,cart_users=self.user,cart_table =self.table)
        self.order_item = OrderItem.objects.create(cart=self.cart, quantity=2,price=20,product=self.pro)
        self.request = HttpRequest()
        self.request.user = self.user
        self.request.session = {'edit_id': self.cart.id}

    def test_staff_panel_waiting_post(self):
        item, carts = StaffPanel.waiting_post(Cart)
        self.assertEqual(item, [self.order_item])
        self.assertEqual(carts, [self.cart])

    def test_accept_ord(self):
        self.request.POST['accepted_ord'] = 'true'
        item, carts = StaffPanel.accept_ord(self.request)
        self.assertEqual(item, [self.order_item])
        self.assertEqual(carts, [self.cart])

    def test_refuse_ord(self):
        self.request.POST['refused_ord'] = 'true'
        item, carts = StaffPanel.refuse_ord(self.request)
        self.assertEqual(item, [self.order_item])
        self.assertEqual(carts, [self.cart])

    def test_get_ord_by_phone(self):
        self.request.POST['phone_number'] = '1234567890'
        item_list, cart_list = StaffPanel.get_ord_by_phone(self.request)
        self.assertEqual(item_list, [self.order_item])
        self.assertEqual(cart_list, [self.cart])

    def test_make_refuse(self):
        self.request.POST['refuse'] = str(self.cart.id)
        StaffPanel.make_refuse(self.request, Cart)
        updated_cart = Cart.objects.get(id=self.cart.id)
        self.assertEqual(updated_cart.status, 'r')
        self.assertEqual(updated_cart.cart_users, self.user)

    def test_make_accept(self):
        self.request.POST['accept'] = str(self.cart.id)
        StaffPanel.make_accept(self.request, Cart)
        updated_cart = Cart.objects.get(id=self.cart.id)
        self.assertEqual(updated_cart.status, 'a')
        self.assertEqual(updated_cart.cart_users, self.user)

    def test_staff_edit_ord_getordforedit(self):
        self.request.session['edit_id'] = self.cart.id
        item, cart_number = StaffEditOrd.get_ord_for_edit(self.request, Cart)
        self.assertEqual(item[0][0], self.order_item)
        self.assertEqual(cart_number, self.cart.customer_number)

    def test_remove_ord(self):
        self.request.session['edit_id'] = self.cart.id
        self.request.POST['remove'] = str(self.order_item.id)
        removed = StaffEditOrd.remove_ord(self.request, Cart)
        self.assertTrue(removed)

    def test_save_new_quantity(self):
        self.request.POST[str(self.order_item.id)] = '2'
        saved = StaffEditOrd.save_new_quantity(self.request, OrderItem)
        updated_order_item = OrderItem.objects.get(id=self.order_item.id)
        updated_cart = Cart.objects.get(id=self.cart.id)
        self.assertTrue(saved)
        self.assertEqual(updated_order_item.quantity, 2)
        self.assertEqual(updated_order_item.cart.total_price, 100)
        self.assertEqual(updated_order_item.cart.total_quantity, 3)

    def test_staff_add_ord_showproductincat(self):
        category = self.cat
        product = self.pro
        self.request.POST['category'] = 'category'
        cat, product_cat = StaffAddOrd.show_product_in_cat(self.request, Product, Category)
        self.assertEqual(cat, [category])
        self.assertEqual(product_cat, [product])

    def test_add_ord_to_shop_cart(self):
        self.request.session['edit_id'] = self.cart.id
        self.request.POST['add'] = str(self.order_item.id)
        self.request.POST['quantity'] = '2'
        added = StaffAddOrd.add_ord_to_shop_cart(self.request, OrderItem)
        updated_cart = Cart.objects.get(id=self.cart.id)
        self.assertTrue(added)
        self.assertEqual(updated_cart.total_price, 30)
        self.assertEqual(updated_cart.total_quantity, 2)

    def test_export_csv_generatecsvresponse(self):
        data = [[1, 2, 3], [4, 5, 6]]
        header = ['A', 'B', 'C']
        filename = 'test_file'
        response = ExportCsv.generate_csv_response(data, header, filename)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get('Content-Disposition'),
            f'attachment; filename="{filename}.csv"'
        )

    def test_customer_getordbyphone(self):
        self.request.POST['tel'] = '1234567890'
        item_list, cart_list = Customer.get_ord_by_phone(self.request, Cart)
        self.assertEqual(item_list, [[self.order_item]])
        self.assertEqual(cart_list, [self.cart])

    def test_manager_statuscount(self):
        today = datetime.today().date()
        accepted_carts_count = Manager.status_count(self.request, today, Cart)
        self.assertEqual(accepted_carts_count['accepted_count'], 0)
        self.assertEqual(accepted_carts_count['refused_count'], 0)
        self.assertEqual(accepted_carts_count['accepted_percentage'], 0.0)
        self.assertEqual(accepted_carts_count['refused_percentage'], 0.0)

    def test_status_order(self):
        today = datetime.today().date()
        status_count = Manager.status_order(request=self.request,today= today,model= Cart)
        self.assertEqual(status_count['accepted_count'], 0)
        self.assertEqual(status_count['refused_count'], 0)
        self.assertEqual(status_count['waiting_count'], 1)
