from django.db import models
from cafe.staff.models import Staff
from cafe.customer.models import Customer


class Cart(models.Model):
    count = models.IntegerField()
    total_price = models.IntegerField()
    discount = models.IntegerField()
    time = models.TimeField()
    earned_point = models.IntegerField()
    cart_customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    cart_staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='cart')

    def __str__(self):
        return f"{self.total_price} order "