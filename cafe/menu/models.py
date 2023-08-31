from django.db import models
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=60 , unique=True)
    photo = models.ImageField(upload_to='media/category_photos')

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    IS_ACTIVE = "is_active"
    NOT_ACTIVE = "not_active"
    STATUS_CHOICES = [
    (IS_ACTIVE, 'active'),
    (NOT_ACTIVE, 'inactive'),
    ]
    name = models.CharField(max_length=50 ,unique=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    status = models.CharField(max_length=10 , choices=STATUS_CHOICES, default=NOT_ACTIVE)
    photo = models.ImageField(upload_to='media/menu_photos')
    description = models.CharField(max_length=500)
    point = models.PositiveIntegerField(default=0)
    category_menu = models.ForeignKey(Category, on_delete=models.PROTECT)

    product_img = models.ImageField(upload_to='images')

    def img_preview(self):  # new
        return mark_safe(f'<img src = "{self.product_img.url}" width = "75" height = "100"/>')
    

    def __str__(self):
        return f"product : {self.name}  price ={self.price}"






