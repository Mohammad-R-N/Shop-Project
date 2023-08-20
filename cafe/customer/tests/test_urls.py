from django.test import SimpleTestCase
from django.urls import reverse, resolve
from customer.views import *

class TestUrls(SimpleTestCase):
    def test_customer_page_url_is_resolved(self):

        url = reverse('customer-page')
        self.assertEquals(resolve(url).func.view_class, CustomerView)



