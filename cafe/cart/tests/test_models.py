from django.test import TestCase
from cart.models import *

class TestTableModel(TestCase):
    def setUp(self):
        self.table1 = Table.objects.create(table_name='Table 1', status='Available')

    def test_table_str(self):
        self.assertEquals(str(self.table1), 'Table: Table 1')

    def test_table_status_default(self):
        table2 = Table.objects.create(table_name= 'Table 2')
        self.assertEquals(table2.status, 'unavailable')

    def test_table_status(self):
        table2 = Table.objects.create(table_name= 'Table 2', status = 'Available')
        self.assertEquals(table2.status, 'Available')