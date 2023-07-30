from django.db import models
from category.models import Category
from cart.models import Cart
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    status = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='')
    description = models.CharField(max_length=300)
    point = models.IntegerField(default=0)
    category_menu = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True)

    def __str__(self):
        return f"product : {self.name}  price ={self.price}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    menu = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
