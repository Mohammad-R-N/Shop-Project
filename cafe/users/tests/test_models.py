from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import CustomUser

class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(phone_number='09123456789', first_name='John', last_name='Doe', code=1234)

    def test_create_user(self):
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.phone_number, '09123456789')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.user.check_password('password'))
        self.assertIsNotNone(self.user.date_joined)
        self.assertEqual(self.user.code, 1234)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(phone_number='09123456788', password='admin', first_name='Admin', last_name='User')
        self.assertIsInstance(admin, CustomUser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_phone_number_field_validation(self):
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(phone_number='1234567890', password='password', first_name='Jane', last_name='Smith')

        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(phone_number='+989123456789', password='password', first_name='Jane', last_name='Smith')