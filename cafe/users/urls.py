from django.urls import path, include
from .views import *

urlpatterns = [
    path('',users_page,name="users"),
    
]