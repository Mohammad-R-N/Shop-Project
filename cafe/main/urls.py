
from django.urls import path, include
from .views import *

urlpatterns = [
    path('home/',home_page,name="home-page")
]