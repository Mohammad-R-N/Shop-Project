from django.db import models
from cafe.customer.models import Customer
from cafe.staff.models import Staff


# Create your models here.
class Order(models.Model):
    count=models.DecimalField(max_digits=3,decimal_places=0)
    total_price=models.DecimalField(max_digits=9,decimal_places=0)
    discount=models.DecimalField(max_digits=2,decimal_places=2)
    order_time=models.DateTimeField(auto_now_add=True)
    earned_point=models.DecimalField(max_digits=10,decimal_places=0)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    # staff=models.ForeignKey(Staff,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.total_price