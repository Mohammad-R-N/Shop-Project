from django.urls import path, include
from .views import *

urlpatterns = [
    path('',menu_page,name="menu"),
    path('',category,name="category"),
]