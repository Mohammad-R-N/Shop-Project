from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from cart.models import Cart, OrderItem
from .utils import CustomerOption

# Create your views here.
class CustomerView(View):
    def get(self, request):
        return render(request,"customer/customer.html")
      
class CustomerHistory(View):
    template_history = "customer/history.html"

    def get(self, request):
        if request.COOKIES.get('number'):
            result = CustomerOption.show_customer_history(request, Cart, OrderItem)
            context = {"items": result[0], "carts": result[1]}
            return render(request, self.template_history, context)
        else:
            return render(request, self.template_history)