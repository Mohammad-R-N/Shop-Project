from .models import CustomUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password

class UserAuthentication:
    def custom_authenticate(phone_number, password):
        user = get_object_or_404(CustomUser, phone_number = phone_number)
        if user is not None:
            if user.check_password(password):
                return user
            else:
                return None