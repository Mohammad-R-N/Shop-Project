from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from cart.models import Cart, OrderItem

# Create your views here.
class CustomerView(View):
    def get(self, request):
        return render(request,"customer/customer.html")
    def post(self, request):
        pass

class CustomerHistory(View):
    template_history = "customer/history.html"

    def get(self, request):
        if request.COOKIES.get('number'):
            number = request.COOKIES.get('number')
            cart = Cart.objects.all()
            item_list = list()
            cart_list = list()

            for cart_obj in cart:
                if cart_obj.customer_number == number:
                    item = OrderItem.objects.filter(cart=cart_obj).values()
                    item_list.append(item)
                    cart_list.append(cart_obj)

            context = {
                "items": item_list,
                "carts": cart_list
                }
            return render(request, self.template_history, context)
        else:
            return render(request, self.template_history)