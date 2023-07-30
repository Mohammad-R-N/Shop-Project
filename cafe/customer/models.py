from django.db import models


class Customer(models.Model):
    phone_number = models.IntegerField(max_length=11)
    order = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.phone_number} "

