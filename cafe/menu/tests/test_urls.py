from django.test import SimpleTestCase
from django.urls import reverse, resolve
from menu.views import *


class TestUrls(SimpleTestCase):
    def test_menu_url_is_resolved(self):

        url = reverse('menu')
        self.assertEquals(resolve(url).func.view_class, MenuView)


