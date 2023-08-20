from django.db import models
from users.validation import phone_number_validator
from users.models import PhoneNumberField 
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    phone_number = PhoneNumberField(_("phone number"), max_length=14, validators=[phone_number_validator], unique = True)
    order = models.IntegerField(default=0)
    point = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.phone_number} "
