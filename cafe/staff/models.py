from django.db import models


class Users(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_number = models.IntegerField()
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

