from django.test import TestCase
from cart.models import *

class TestTableModel(TestCase):
    def setUp(self):
        self.table = Table.objects.create(table_name='Table 1', status='Available')