from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.authentication import CustomAuthBackend
from users.views import *
from users.forms import *
from unittest.mock import patch
import json
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


class OrderStatusReportViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('order_status_report'))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsInstance(result, dict)

class ManagerDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(phone_number="09123456789", password="pass")
    def test_get_authenticated(self):
        self.client.force_login(self.user) 
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)


    def test_get_not_authenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('staff_login'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are NOT allowed to see staff panel")
        self.assertEqual(messages[0].tags, "danger error")

class MonthlySalesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_to_response(self):
        response = self.client.get(reverse('monthly_sales'))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsInstance(result, dict)
        self.assertIn('months', result)
        self.assertIsInstance(result['months'], list)
        self.assertIn('monthly_sales', result)
        self.assertIsInstance(result['monthly_sales'], list)



class YearlySalesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_to_response(self):
        response = self.client.get(reverse('yearly_sales'))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsInstance(result, dict)
        self.assertIn('years', result)
        self.assertIsInstance(result['years'], list)
        self.assertIn('yearly_sales', result)
        self.assertIsInstance(result['yearly_sales'], list)


class DailySalesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_to_response(self):
        response = self.client.get(reverse('daily_sales'))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsInstance(result, dict)
        self.assertIn('days', result)
        self.assertIsInstance(result['days'], list)
        self.assertIn('daily_sales', result)
        self.assertIsInstance(result['daily_sales'], list)


class TotalSalesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_to_response_json(self):
        response = self.client.get(reverse('total_sales'))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsInstance(result, dict)
        self.assertIn('total_sales', result)

    def test_render_to_response_csv(self):
        response = self.client.get(reverse('total_sales') + '?format=csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="total_sales.csv"')
        self.assertEqual(response.content.decode(), 'Total Sales\nNone')

class TopSellingItemsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_render_to_response_json(self):
        response = self.client.get(reverse('top_selling_items'))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertIsInstance(result, dict)
        self.assertIn('product_names', result)
        self.assertIsInstance(result['product_names'], list)
        self.assertIn('quantities', result)
        self.assertIsInstance(result['quantities'], list)

from django.utils import timezone


class PopularItemsMorningViewTest(TestCase):
    def test_get_queryset(self):
        view = PopularItemsMorningView()
        view.request = None  
        queryset = view.get_queryset()
        start_time = timezone.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        end_time = timezone.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        expected_queryset = OrderItem.objects.filter(cart__time__range=(start_time, end_time)) \
            .values('product__name') \
            .annotate(total_ordered=Sum('quantity')) \
            .order_by('-total_ordered')[:2]
        self.assertQuerysetEqual(queryset, expected_queryset, transform=lambda x: x)

class CustomerHistoryTest(TestCase):
    def setUp(self):
        self.client = Client()

  
    def test_post_with_tel(self):
        response = self.client.post(reverse('history_for_manager'), {'tel': '09123456789'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/history_for_manager.html')
        self.assertIn('items', response.context)
        self.assertIn('carts', response.context)

    def test_post_without_tel(self):
        response = self.client.post(reverse('history_for_manager'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/history_for_manager.html')
        self.assertNotIn('items', response.context)
        self.assertNotIn('carts', response.context)