from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MenuView.as_view(), name="menu"),
    path("search/", search_products, name="search_products"),
    path("product_popup/<int:product_id>/", ProductPopup.as_view(), name="product_popup"),
]