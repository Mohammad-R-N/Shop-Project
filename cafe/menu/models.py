from django.db import models
from cart.models import Cart


class Category(models.Model):
    name = models.CharField(max_length=60)
    photo = models.ImageField(upload_to='media/')

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    IS_ACTIVE = "is_active"
    NOT_ACTIVE = "not_active"
    STATUS_CHOICES = [
    (IS_ACTIVE, 'active'),
    (NOT_ACTIVE, 'inactive'),
    ]
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    status = models.CharField(max_length=10 , choices=STATUS_CHOICES, default=NOT_ACTIVE)
    photo = models.ImageField(upload_to='static/menu_photos')
    description = models.CharField(max_length=500)
    point = models.PositiveIntegerField(default=0)
    category_menu = models.ForeignKey(Category, on_delete=models.PROTECT)
    

    def __str__(self):
        return f"product : {self.name}  price ={self.price}"


class OrderItem(models.Model):
    menu = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6,decimal_places=2)



