from django.test import TestCase
from users.models import CustomUser

class CustomUserManagerTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(phone_number="09123456789", password='pass')


    def test_create_user(self):
        
        self.assertEqual(self.user.phone_number, '09123456789')
        self.assertTrue(self.user.check_password('pass'))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)