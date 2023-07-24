from django.urls import path, include
from .views import *

urlpatterns = [
    path('',cart_page,name="cart-page"),
]