from django.shortcuts import render, redirect
from menu.models import Product
from cart.models import Table, Cart, OrderItem
from django.views import View
from django.contrib import messages
from .utils import ProductOption, Reservation, OrderDetail

class CartView(View):
    def get(self, request):
        if request.COOKIES.get('product') is not None:
            result = ProductOption.show_product(request, Product)
            context = {'product': result[1], 'sub_total': result[0],}
            return render(request, "cart/cart.html", context)
        else:
            return render(request, "cart/cart.html")
        
    def post(self, request):
        if "remove" in request.POST:
            ProductOption.remove_from_shop_cart(request)
        elif "done" in request.POST:
            ProductOption.accept_shop_cart(request)
        else:
            return redirect('home')
        
class ReservationView(View):
    template_name = "customer/reserve.html"
    def get(self, request):
        tables = Table.objects.all()
        context = {'table': tables, 'total': request.session['cost']}
        return render(request, self.template_name, context)
    
    def post(self, request):
        result = Reservation.checkout(request, Product, Table, Cart, OrderItem)
        return result

class OrdDetail(View):
    template_name = "customer/customer_ord_detail.html"

    def get(self, request):
        if request.COOKIES.get('number'):
            result = OrderDetail.show_cart_detail(request, Cart, OrderItem)
            context = {"cart": result[1], "items": result[0], "process": result[2]}
            messages.success(request, 'Your ORDER has send successfully!', 'success')
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)

