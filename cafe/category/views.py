from django.shortcuts import render
from . models import Category
# Create your views here.
def category():
    cat = Category.objects.all()
    return cat
