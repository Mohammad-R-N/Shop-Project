from django.urls import path, include
from .views import *

urlpatterns = [
    path('', CartView.as_view(), name="cart"),
    path('reserve/', ReservationView.as_view(), name="reservation"),
    path('detail/', OrdDetail.as_view(), name="ord_detail"),
]