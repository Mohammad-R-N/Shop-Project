from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MenuView.as_view(), name="menu"),
]