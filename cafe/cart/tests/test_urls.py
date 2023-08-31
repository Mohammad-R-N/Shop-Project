from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart.views import *

class TestUrls(SimpleTestCase):
    def test_cart_url_is_resolved(self):

        url = reverse('cart')
        self.assertEquals(resolve(url).func.view_class, CartView)

    def test_reservation_url_is_resolved(self):

        url = reverse('reservation')
        self.assertEquals(resolve(url).func.view_class, ReservationView)

    def test_orddetail_url_is_resolved(self):

        url = reverse('ord_detail')
        self.assertEquals(resolve(url).func.view_class, OrdDetail)

    