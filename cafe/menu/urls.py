from django.urls import path, include
from .views import *

urlpatterns = [
    path("", menu_page, name="menu"),
    path("", category, name="category"),
    path("search/", search_products, name="search_products"),
    path("product_popup/<int:product_id>/", product_popup, name="product_popup"),
]
