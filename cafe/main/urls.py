
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',home_page,name="home-page"),
    path("cart/",include("cart.urls")),
    path("menu/",include("menu.urls")),
    path("staff/",include("staff.urls")),
    path("customer/",include("customer.urls")),
    path("category/",include("category.urls"))
]