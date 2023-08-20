from django.test import TestCase
from customer.models import *
from django.core.exceptions import ValidationError

class TestCustomerModel(TestCase):
    def setUp(self) -> None:
        self.customer1 = Customer.objects.create( phone_number = "09123456789")


    def test_customer_str(self):
        self.assertEquals(str(self.customer1.phone_number), '09123456789')

    def test_Customer_phone_number_max_length(self):
        max_length = Customer._meta.get_field('phone_number').max_length
        self.assertEqual(max_length, 14)
    
    

    def test_customer_number_validation(self):
        customer2 = Customer(phone_number = "0912", order = 0, point = 0 )
        with self.assertRaises(ValidationError) as err:
            customer2.full_clean() 
        self.assertEqual(err.exception.message_dict['phone_number'], ["Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."])

    def test_order_default(self):
        self.assertEquals(self.customer1.order , 0)

    def test_point_default(self):
        self.assertEquals(self.customer1.point , 0)

