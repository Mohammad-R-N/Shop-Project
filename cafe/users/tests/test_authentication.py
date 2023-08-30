from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from users.authentication import CustomAuthBackend

class CustomAuthBackendTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(phone_number='09123456789', password = "pass")

    def test_authenticate_existing_user_with_correct_code(self):
        request = self.factory.get('/')
        user = CustomAuthBackend.authenticate(request, phone_number='09123456789', password = "pass")
        self.assertEqual(user, self.user)

    def test_authenticate_non_existing_user(self):
        request = self.factory.get('/')
        user = CustomAuthBackend.authenticate(request, phone_number='09123456711', password = "pass")
        self.assertIsNone(user)

    def test_authenticate_existing_user_with_incorrect_code(self):
        request = self.factory.get('/')
        user = CustomAuthBackend.authenticate(request, phone_number='09123456789', code='5678')
        self.assertIsNone(user)
    
    def test_action_when_user_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)