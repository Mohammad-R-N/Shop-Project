from django.db import models

# Create your models here.
class Customer(models.Model):
    phone=models.DecimalField(max_digits=11,decimal_places=0)
    points=models.DecimalField(max_digits=10,decimal_places=0)

    def __str__(self) -> str:
        return self.phone