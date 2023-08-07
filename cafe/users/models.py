from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    phone_number = models.CharField(_("phone number"), max_length=20, unique=True)
    first_name = models.CharField(_("first name"), max_length=20)
    last_name = models.CharField(_("first name"), max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    

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