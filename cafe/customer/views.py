from django.shortcuts import render, redirect, HttpResponse
from django.views import View


# Create your views here.
class CustomerView(View):
    def get(self, request):
        return render(request,"customer/customer.html")
    def post(self, request):
        pass