from django.contrib import admin
from .models import CustomUser
from .models import Users

admin.site.register(CustomUser)
admin.site.register(Users)