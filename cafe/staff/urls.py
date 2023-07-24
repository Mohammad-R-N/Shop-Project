from django.urls import path, include
from .views import *

urlpatterns = [
    path('',staff_page,name="staff-page"),
]