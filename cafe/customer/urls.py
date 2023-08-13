from django.urls import path, include
from .views import *

urlpatterns = [
    path('', CustomerView.as_view(), name="customer-page"),
    path('history', CustomerHistory.as_view(), name="customer-history"),
]