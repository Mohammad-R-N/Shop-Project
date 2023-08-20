from django.test import TestCase, Client
from django.urls import reverse
from home.models import SiteConfig



class TestHomerView(TestCase):

    def setUp(self):
        self.client= Client()
        self.home_url = reverse('home')
        self.default_view_url = reverse('main')
        self.logo_view_url = reverse('logo')
        self.site_config = SiteConfig.objects.create(logo="test.png")

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main.html')

    def test_default_view_GET(self):
        response = self.client.get(self.default_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main.html')

    def test_logo_view_GET(self):
        response = self.client.get(self.logo_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_logo_view_context(self):
        response = self.client.get(self.logo_view_url)
        self.assertEqual(response.context['site_config'], self.site_config)
        