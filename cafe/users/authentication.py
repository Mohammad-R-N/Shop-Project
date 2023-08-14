from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

class CustomAuthBackend(BaseBackend):
    @staticmethod
    def authenticate(request, phone_number=None, code=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None

        if user.code == code:
            return user
        else:
            return None
