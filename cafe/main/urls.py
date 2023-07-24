
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',home_page,name="home-page"),
    path("cart/",include("cart.urls")),
    path("menu/",include("menu.urls"),name="menu-page"),
    path("staff/",include("staff.urls"),name="staff-page"),
    path("customer/",include("customer.urls"),name="customer-page"),
    path("category/",include("category.urls"))
]