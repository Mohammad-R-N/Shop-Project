from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
import re
from .validation import phone_number_validator
from .models import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "first_name","last_name", "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["phone_number", "password"]

class StaffLoginForm(forms.Form):
    phone_number = PhoneNumberField(unique = True, max_length=19, validators=[phone_number_validator])

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        formatted_phone_number = re.sub(r'^0098|^\+98', '09', phone_number)
        return formatted_phone_number

class StaffOtpForm(forms.Form):
    code=forms.IntegerField()

