from django.test import TestCase
from cart.models import *
from decimal import Decimal
from django.core.exceptions import ValidationError


"""
    Table Model Tests
"""
class TestTableModel(TestCase):
    def setUp(self):
        self.table1 = Table.objects.create(table_name='Table 1', status='Available')

    def test_table_str(self):
        self.assertEquals(str(self.table1), 'Table: Table 1')

    def test_table_status_default(self):
        table2 = Table.objects.create(table_name= 'Table 2')
        self.assertEquals(table2.status, 'unavailable')

    def test_table_status(self):
        table2 = Table.objects.create(table_name= 'Table 2', status = 'Available')
        self.assertEquals(table2.status, 'Available')

    def test_table_update_status(self):
        self.table1.status = 'unavailable'
        self.table1.save()
        self.assertEqual(self.table1.status, 'unavailable')

    def test_table_status_max_length(self):
        max_length = Table._meta.get_field('status').max_length
        self.assertEqual(max_length, 20)

    def test_table_name_max_length(self):
        max_length = Table._meta.get_field('table_name').max_length
        self.assertEqual(max_length, 100)

    def test_table_status_choices(self):
        choices = [choice[0] for choice in Table.STATUS_CHOICES]
        self.assertListEqual(choices, ['Available', 'unavailable'])

    def test_table_each_status(self):
        self.assertEqual(Table.Available, 'Available')
        self.assertEqual(Table.unavailable, 'unavailable')


"""
    Cart Model Tests
"""
class TestCartModel(TestCase):
    def setUp(self):
        self.cart1 = Cart.objects.create(
            total_price=Decimal('0.00'),
            total_quantity=0,
            customer_number='+989123456789',
            cart_users=None,
            cart_table=Table.objects.create(table_name = 'test table'),
        )

    def test_cart_str(self):
        self.assertEquals(str(self.cart1), "0 order ")

    def test_cart_each_status(self):
        self.assertEqual(Cart.ACCEPT, 'a')
        self.assertEqual(Cart.REFUSE, 'r')
        self.assertEqual(Cart.WAITING, 'w')

    def test_cart_status_default(self):
        self.assertEquals(self.cart1.status, 'w')

    def test_cart_status_max_length(self):
        max_length = Cart._meta.get_field('status').max_length
        self.assertEqual(max_length, 1)

    def test_cart_total_price_max_length(self):
        max_digits = Cart._meta.get_field('total_price').max_digits
        self.assertEqual(max_digits, 6)

    def test_cart_customer_number_max_length(self):
        max_length = Cart._meta.get_field('customer_number').max_length
        self.assertEqual(max_length, 14)

    def test_cart_update_status(self):
        self.cart1.status = 'a'
        self.cart1.save()
        self.assertEqual(self.cart1.status, 'a')

    def test_new_cart_has_custom_status(self):
        cart2 = Cart.objects.create(
            total_price=Decimal('0.00'),
            total_quantity=0,
            customer_number='09123456789',
            cart_users=None,
            cart_table=Table.objects.create(table_name = "test table"),
            status=Cart.ACCEPT,
        )
        self.assertEqual(cart2.status, Cart.ACCEPT)

    def test_cart_can_have_user(self):
        user2 = CustomUser.objects.create(
            phone_number = "09191234567",
            
        )
        cart2 = Cart.objects.create(
                total_price=Decimal('0.00'),
                total_quantity=0,
                customer_number='09123456789',
                cart_users=user2,
                cart_table=Table.objects.create(table_name = "test table"),
            )
        
        self.assertEquals(cart2.cart_users , user2)

    def test_cart_can_have_table(self):
        table2 = Table.objects.create(table_name = "test table")
        cart2 = Cart.objects.create(
            total_price=Decimal('0.00'),
            total_quantity=0,
            customer_number='09123456789',
            cart_users=None,
            cart_table=table2,
        )
        self.assertEqual(cart2.cart_table, table2)

    def test_customer_number_validation(self):
        cart = Cart(
            total_price=Decimal('0.00'),
            total_quantity=0,
            customer_number='123',  
            cart_users=None,
            cart_table=Table.objects.create(table_name = "test table"),
        )
        with self.assertRaises(ValidationError) as err:
            cart.full_clean() #when i dont wanna validate data in forms and only if i wanna handle exceptions myself
        self.assertEqual(err.exception.message_dict['customer_number'], ["Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."])

    def test_cart_foreignkey_protect(self):
   
        for f in self.cart1._meta.get_fields():
            if isinstance(f, models.ForeignKey):
                self.assertEquals(f.remote_field.on_delete, models.PROTECT,
                                '{} failed, value was {}'.format(
                                    f.name, f.remote_field.on_delete))