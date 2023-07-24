from django.urls import path, include
from .views import *

urlpatterns = [
    path('',category_page,name="category-page"),
]