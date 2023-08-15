from django.shortcuts import render, redirect
from menu.models import Product
from cart.models import Table, Cart, OrderItem
from django.views import View
from django.contrib import messages

class CartView(View):
    cost = 0
    def get(self, request):
        product_list = list()

        if request.COOKIES.get('product') is not None:
            result = request.COOKIES.get('product')
            result = str(result).split('-')
            result.pop(0)
            
            for name in result:
                pt_name = name.split('=')
                product = Product.objects.get(name=pt_name[0])
                data = dict()
                data['product_name'] = product.name
                data['product_photo'] = product.photo.url
                data['product_price'] = product.price
                data['product_quantity'] = pt_name[1]
                data['total'] = int(pt_name[1]) * product.price
                product_list.append(data)

            for pt in product_list:
                self.cost += pt['total']
            
            request.session['total'] = str(self.cost)
            context = {
                'product': product_list,
                'sub_total': self.cost,
            }
            return render(request, "cart/cart.html", context)
        
        else:
            return render(request, "cart/cart.html")
        
    def post(self, request):
        if "remove" in request.POST:
            remove = request.POST['remove']
            result = request.COOKIES.get('product')
            result = str(result).split('-')
            result.pop(0)
            new_cookie = ''

            for name in result:
                pt_name = name.split('=')
                if pt_name[0] == remove:
                    pass
                else:
                    new_cookie += f"-{pt_name[0]}={pt_name[1]}"
            try:
                response = redirect("cart")
                response.set_cookie(key='product', value=new_cookie)
                return response
            except:
                response = redirect("cart")
                response.set_cookie(key='product', value='')
                return response
        
        elif "done" in request.POST:
            if request.COOKIES.get('product') is not None:
                if len(request.COOKIES.get('product')) > 1:
                    result = request.COOKIES.get('product')
                    result = str(result).split('-')
                    result.pop(0)
                    request.session['order'] = result
                    request.session['cost'] = request.session['total']
                    del request.session['total']
                    return redirect('reservation')
                else:
                    return redirect('cart')
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

        user = request.user
        table = request.POST['subject']
        phone_number = request.POST['tel']

        table_obj = Table.objects.get(table_name=table)          
        cart = Cart.objects.create(total_price=cost, total_quantity=len(order), 
                                    customer_number=phone_number, cart_users=user, cart_table=table_obj)
        cart.save()

        for ord in order:
            pt_name = ord.split('=')
            pt = Product.objects.get(name=pt_name[0])
            order_item = OrderItem.objects.create(product=pt, cart=cart, quantity=pt_name[1], price=pt.price)
            order_item.save()

        result = redirect('ord_detail')
        result.set_cookie("number", phone_number, 365)
        result.delete_cookie('product')
        return result

class OrdDetail(View):
    template_name = "customer/customer_ord_detail.html"

    def get(self, request):
        if request.COOKIES('number') is not None:
            # phone_number = request.session['number']
            cart = Cart.objects.all()
            item = list()
            cart_list = list()
            for cart in cart:
                if cart.customer_number == phone_number:
                    items = OrderItem.objects.filter(cart=cart)
                    cart_list.append(cart)
                    item.append(items)


            context = {
                "cart": cart_list,
                "items": item,
                "process": "Waiting for accepting from Staff"
            }
            messages.success(request, 'Your ORDER has send successfully!', 'success')
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)

