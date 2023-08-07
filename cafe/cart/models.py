from django.db import models
from users.models import Users
from users.models import CustomUser
from customer.models import Customer
from menu.models import Product


class Table(models.Model):
    Available = "Available"
    unavailable = "unavailable"
    
    STATUS_CHOICES = [
    (Available, 'Available'),
    (unavailable, 'unavailable'),
    ]
    
    table_name = models.CharField(max_length=100)
    table_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES, default=unavailable) 
       
    def __str__(self):
        return f"{self.table_name} order "
    
class Cart(models.Model):
    total_price = models.DecimalField(max_digits=6,decimal_places=2)
    discount = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    total_quantity = models.PositiveIntegerField()
    earned_point = models.PositiveIntegerField(default=0)
    cart_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_users = models.ForeignKey(Users, on_delete=models.PROTECT)
    cart_staff = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    cart_table = models.ForeignKey(Table, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.total_price} order "
    
    

class OrderItem(models.Model):
    menu = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2)