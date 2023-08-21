from django.test import TestCase
from users.models import CustomUser

class CustomUserManagerTests(TestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(phone_number="09123456789", password='pass')


