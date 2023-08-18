from django.shortcuts import render, redirect
from menu.models import Product
from cart.models import Table, Cart, OrderItem
from django.views import View
from django.contrib import messages
from .utils import ProductOption

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
    def get(self, request):
        tables = Table.objects.all()
        context = {
            'table': tables,
            'total': request.session['cost']
        }
        return render(request, "customer/reserve.html", context)
    
    def post(self, request):
        cost = request.session['cost']
        del request.session['cost']

        order = request.session['order']
        del request.session['order']

        table = request.POST['subject']
        phone_number = request.POST['tel']

        table_obj = Table.objects.get(table_name=table)          
        cart = Cart.objects.create(total_price=cost, total_quantity=len(order), 
                                    customer_number=phone_number, cart_table=table_obj)
        cart.save()

        for ord in order:
            pt_name = ord.split('=')
            pt = Product.objects.get(name=pt_name[0])
            order_item = OrderItem.objects.create(product=pt, cart=cart, quantity=pt_name[1], price=pt.price)
            order_item.save()

        result = redirect('ord_detail')
        result.set_cookie("number", phone_number, 2630000)
        result.delete_cookie('product')
        return result

class OrdDetail(View):
    template_name = "customer/customer_ord_detail.html"

    def get(self, request):
        if request.COOKIES.get('number'):
            phone_number = request.COOKIES.get('number')
            cart = Cart.objects.all()
            item = list()
            cart_list = list()
            status = list()
            for cart_obj in cart:
                if cart_obj.customer_number == phone_number:
                    items = OrderItem.objects.filter(cart=cart_obj)
                    cart_list.append(cart_obj)

                    item.append(items[0])
                    if cart_obj.status == "w":
                        status.append("Waiting for accept from Admin")
                    elif cart_obj.status == "a":
                        status.append("Accepted from Admin")
                    elif cart_obj.status == "r":
                        status.append("Refused from Admin")

            context = {
                "cart": cart_list,
                "items": item,
                "process": status
            }
            messages.success(request, 'Your ORDER has send successfully!', 'success')
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)

