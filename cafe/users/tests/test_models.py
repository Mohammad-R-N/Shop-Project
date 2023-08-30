from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import CustomUser

class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(phone_number='09123456789',password="Pa33Word", first_name='John', last_name='Doe', code=1234)

    def test_create_user(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.phone_number, '09123456789')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.check_password('Pa33Word'))
        self.assertIsNotNone(self.user.date_joined)
        self.assertEqual(self.user.code, 1234)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(phone_number='09123456788', password='admin', first_name='Admin', last_name='User')
        self.assertIsInstance(admin, CustomUser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_phone_number_field_validation(self):
        
        myuser = CustomUser(
            phone_number = '123',
            password = "pass",
        )
        with self.assertRaises(ValidationError) as err:
            myuser.full_clean()
        self.assertEqual(err.exception.message_dict['phone_number'], ["Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."])