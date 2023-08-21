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






