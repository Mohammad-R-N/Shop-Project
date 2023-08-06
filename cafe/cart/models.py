from django.db import models
from staff.models import Staff
from customer.models import Customer

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
    
    
class Table(models.Model):
    Available = "Available"
    unavailable = "unavailable"
    
    STATUS_CHOICES = [
    (Available, 'Available'),
    (unavailable, 'unavailable'),
    ]
    
    table_name = models.CharField(max_length=100)
    table_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=10 , choices=STATUS_CHOICES, default=unavailable)    

    
