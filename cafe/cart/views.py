from django.shortcuts import render, redirect
from menu.models import Product
from cart.models import Table, Cart, OrderItem
from django.views import View
from django.contrib import messages
from .utils import ProductOption, Reservation, OrderDetail

class CartView(View):
    def get(self, request):
        if request.COOKIES.get('product') is not None:
            result = ProductOption.show_product(self,request, Product)
            context = {'product': result[1], 'sub_total': result[0],}
            return render(request, "cart/cart.html", context)
        else:
            return render(request, "cart/cart.html")
        
    def post(self, request):
        if "remove" in request.POST:
            new_info = ProductOption.remove_from_shop_cart(self,request)
            try:
                response = redirect("cart")
                response.set_cookie(key='product', value=new_info)
                return response
            except:
                response = redirect("cart")
                response.set_cookie(key='product', value='')
                return response
        elif "done" in request.POST:
            res = ProductOption.accept_shop_cart(self,request)
            if res:
                return redirect('reservation')
            else:
                return redirect('cart')
        else:
            return redirect('home')
        
class ReservationView(View):
    template_name = "customer/reserve.html"
    def get(self, request):
        tables = Table.objects.all()
        context = {'table': tables, 'total': request.session['cost']}
        return render(request, self.template_name, context)
    
    def post(self, request):
        phone = Reservation.checkout(self,request, Product, Table, Cart, OrderItem)
        result = redirect('ord_detail')
        result.set_cookie("number", phone, 2630000)
        result.delete_cookie('product')
        return result

class OrdDetail(View):
    template_name = "customer/customer_ord_detail.html"

    def get(self, request):
        if request.COOKIES.get('number'):
            result = OrderDetail.show_cart_detail(self,request, Cart, OrderItem)
            context = {"cart": result[1], "items": result[0], "process": result[2]}
            messages.success(request, 'Your ORDER has send successfully!', 'success')
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)

