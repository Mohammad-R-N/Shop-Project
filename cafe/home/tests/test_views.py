from django.test import TestCase, Client
from django.urls import reverse
from home.models import SiteConfig



class TestHomerView(TestCase):

    def setUp(self):
        self.client= Client()
        self.home_url = reverse('home')


