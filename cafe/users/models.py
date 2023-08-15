from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from .validation import phone_number_validator
from django.core.exceptions import ValidationError
import re



class PhoneNumberField(models.CharField):
    def get_prep_value(self, value):
        if value is None:
            return value

        try:
            regex = phone_number_validator(value)
        except ValidationError:
            raise ValidationError("Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'.")

        formatted_phone_number = re.sub(r'^\+98|^0098', '0', value)
        return formatted_phone_number

class CustomUser(AbstractBaseUser, PermissionsMixin):

    phone_number = PhoneNumberField(_("phone number"), max_length=14, unique=True, validators=[phone_number_validator])
    first_name = models.CharField(_("first name"), max_length=20)
    last_name = models.CharField(_("first name"), max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    code=models.PositiveSmallIntegerField(null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
    
