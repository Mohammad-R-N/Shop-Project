from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import *


class TestUrls(SimpleTestCase):
    def test_staff_url_is_resolved(self):

        url = reverse('staff')
        self.assertEquals(resolve(url).func.view_class, StaffPanelView)

    def test_edit_ord_url_is_resolved(self):
        url = reverse('edit_ord')
        self.assertEquals(resolve(url).func.view_class, EditOrder)

    def test_add_ord_url_is_resolved(self):
        url = reverse('add_ord')
        self.assertEquals(resolve(url).func.view_class, AddOrder)

    def test_staff_login_url_is_resolved(self):
        url = reverse('staff_login')
        self.assertEquals(resolve(url).func.view_class, StaffLogin)

    def test_check_otp_url_is_resolved(self):
        url = reverse('check-otp')
        self.assertEquals(resolve(url).func.view_class, CheckOtp)

    def test_logout_user_url_is_resolved(self):
        url = reverse('logout_user')
        self.assertEquals(resolve(url).func.view_class, LogOutView)

    def test_dashboard_url_is_resolved(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func.view_class, manager_dashboard)

    def test_popular_items_url_is_resolved(self):
        url = reverse('popular_items')
        self.assertEquals(resolve(url).func.view_class, PopularItemsView)

    def test_sales_by_customer_url_is_resolved(self):
        url = reverse('sales_by_customer')
        self.assertEquals(resolve(url).func.view_class, SalesByCustomerView)

    def test_peak_business_hour_url_is_resolved(self):
        url = reverse('peak_business_hour')
        self.assertEquals(resolve(url).func.view_class, PeakBusinessHourView)

    def test_sales_by_employee_url_is_resolved(self):
        url = reverse('sales_by_employee')
        self.assertEquals(resolve(url).func.view_class, SalesByEmployeeView)

    def test_history_for_manager_url_is_resolved(self):
        url = reverse('history_for_manager')
        self.assertEquals(resolve(url).func.view_class, CustomerHistory)









