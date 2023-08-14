from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.validation import phone_number_validator
from users.models import PhoneNumberField 
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
    status = models.CharField(max_length=20 , choices=STATUS_CHOICES, default=unavailable)

    def __str__(self):
        return f"{self.table_name} order "
    
class Cart(models.Model):
    total_price = models.DecimalField(max_digits=6,decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    total_quantity = models.PositiveIntegerField()
    customer_number = PhoneNumberField(_("phone number"), max_length=14, unique=True, validators=[phone_number_validator])
    cart_users = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    cart_table = models.ForeignKey(Table, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.total_price} order "
    
class OrderItem(models.Model):
    menu = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2)