from django.urls import path, include
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("cart/", include("cart.urls")),
    path("menu/", include("menu.urls")),
    path("users/", include("users.urls")),
    path("customer/", include("customer.urls")),
    path("home", DefaultView.as_view(), name="main"),
    path("logo/", LogoView.as_view(), name="logo"),
]
