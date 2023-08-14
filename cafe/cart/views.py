from django.shortcuts import render, redirect, HttpResponse
from menu.models import Product
from cart.models import Table
from django.views import View

# Create your views here.
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
        ord_list = list()
        if request.session.has_key('reserve'):
            if request.session['reserve'] is not None:
                reserve_ord = request.session['reserve']
                for ord in reserve_ord:
                    ord_list.append(ord)
                cost = request.session['cost']
                del request.session['cost']
                order = request.session['order']
                del request.session['order']
                table = request.POST['subject']
                phone_number = request.POST['tel']

                if table == '1':
                    table = 1
                elif table == '2':
                    table = 2
                elif table == '3':
                    table = 3
                elif table == '4':
                    table = 4
                elif table == '5':
                    table = 5

                reserve_info = {
                'table': table,
                'cost': cost,
                'phone_number': phone_number,
                'orders': order,
                }
                ord_list.append(reserve_info)
                request.session['reserve'] = ord_list
                # del request.session['reserve']
        else:
            cost = request.session['cost']
            del request.session['cost']
            order = request.session['order']
            del request.session['order']
            table = request.POST['subject']
            phone_number = request.POST['tel']

            if table == '1':
                table = 1
            elif table == '2':
                table = 2
            elif table == '3':
                table = 3
            elif table == '4':
                table = 4
            elif table == '5':
                table = 5

            reserve_info = {
            'table': table,
            'cost': cost,
            'phone_number': phone_number,
            'date': str(date),
            'orders': order,
            }
            ord_list.append(reserve_info)
            request.session['reserve'] = ord_list

            # del request.session['reserve']
        result = redirect('ord_detail')
        result.delete_cookie('product')
        return result

class OrdDetail(View):
    template_name = "customer/customer_ord_detail.html"

    def get(self, request):
        product_list = list()
        order = request.session['reserve'][-1]
        for name in order['orders']:
                pt_name = name.split('=')
                product = Product.objects.get(name=pt_name[0])
                data = dict()
                data['product_name'] = product.name
                data['product_photo'] = product.photo.url
                data['product_price'] = product.price
                data['product_quantity'] = pt_name[1]
                data['total'] = int(pt_name[1]) * product.price
                product_list.append(data)
        context = {
            "product_info": product_list,
            "user_info": order['table'],
            "process": "Waiting for accepting from Staff"
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        pass