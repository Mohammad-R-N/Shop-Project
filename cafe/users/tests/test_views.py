from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.authentication import CustomAuthBackend
from users.views import *
from users.forms import *
from unittest.mock import patch

class StaffLoginTestCase(TestCase):
    def test_get_staff_login(self):
        response = self.client.get(reverse("staff_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "staff/login.html")
        self.assertEqual(response.context["form"], StaffLoginForm)

    def test_post_staff_login_valid(self):
        response = self.client.post(
            reverse("staff_login"),
            {"phone_number": "09123456789"},
        )
        self.assertEqual(response.status_code, 302)

class LogOutViewTestCase(TestCase):
    def test_get_logout_view(self):
        user = CustomUser.objects.create_user(phone_number="09123456789", password="pass")
        self.client.force_login(user)
        response = self.client.get(reverse("logout_user"), follow=True)
        self.assertRedirects(response, reverse("staff_login"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "LogOut Successfully!")




class CheckOtpTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('check-otp')  

    def test_get_method_renders_form(self):
        request = self.factory.get(self.url)
        response = CheckOtp.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_post_invalid_form(self):
        request = self.factory.post(self.url, {'code': ''})

        response = CheckOtp.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('menu'))