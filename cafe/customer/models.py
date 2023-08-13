from django.db import models


class Customer(models.Model):
    phone_number = models.CharField(max_length=14, unique=True)
    order = models.IntegerField(default=0)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.phone_number} "

