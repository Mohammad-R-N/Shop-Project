from django.db import models
from cart.models import Cart


class Category(models.Model):
    name = models.TextField(max_length=60)
    photo = models.ImageField(upload_to='media/img')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    
    STATUS_CHOICES = [
    (True, 'active'),
    (False, 'inactive'),
    ]
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    status = models.CharField(max_length=5 , choices=STATUS_CHOICES, default="False")
    photo = models.ImageField(upload_to='static/menu_photos')
    description = models.CharField(max_length=500)
    point = models.PositiveIntegerField(default=0)
    category_menu = models.ForeignKey(Category, on_delete=models.PROTECT)
    

    def __str__(self):
        return f"product : {self.name}  price ={self.price}"


class OrderItem(models.Model):
    menu = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)



