
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',home_page,name="home"),
    path("cart/",include("cart.urls")),
    path("menu/",include("menu.urls")),
    path("users/",include("users.urls")),
    path("customer/",include("customer.urls")),
    
]