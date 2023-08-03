from django.urls import path, include
from .views import *

urlpatterns = [
    path('',customer_page,name="customer-page"),
    path('reserve/',reservation,name="reservation"),
]