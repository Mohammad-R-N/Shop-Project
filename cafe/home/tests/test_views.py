from django.test import TestCase, Client
from django.urls import reverse
from home.models import SiteConfig



class TestHomerView(TestCase):

    def setUp(self):
        self.client= Client()
        self.home_url = reverse('home')

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main.html')
