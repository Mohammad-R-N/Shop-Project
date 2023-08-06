from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(_("phone number"), max_length=20, unique=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
    
class Users(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to="media/users_photos")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"