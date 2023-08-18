from django.test import TestCase
from cart.models import *

class TestTableModel(TestCase):
    def setUp(self):
        self.table1 = Table.objects.create(table_name='Table 1', status='Available')

    def test_table_str(self):
        self.assertEquals(str(self.table1), 'Table: Table 1')