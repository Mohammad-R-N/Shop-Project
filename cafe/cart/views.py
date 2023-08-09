from django.shortcuts import render, redirect
from menu.models import Product
from django.views import View

# Create your views here.
class CartView(View):
    def get(self, request):
        if request.COOKIES.get('product') is not None:
            result = request.COOKIES.get('product')
            result = str(result).split('-')
            # res_quantity = request.COOKIES.get('quantity')
            # res_quantity = str(res_quantity).split('-') #'2-3-5-1-1-1'
            # print(res_quantity  )
            # quantity = list()
            # for n in res_quantity:
            #     print(n)
            #     quantity.append(int(n))
            product_list = list()
            # quantity_list = list()
            for name in result:
                product = Product.objects.get(name=name)
                product_list.append(product)
            context = {
                'product': product_list,
                # 'quantity': quantity_list
            }
            return render(request, "cart/cart.html", context)
        else:
            return render(request, "cart/cart.html")
        
    def post(self, request):
        if "done" in request.POST:
            product_list = list()
            cost = 0
            if request.COOKIES.get('product') is not None:
                # if request.COOKIES.get('quantity') is not None:
                    result = request.COOKIES.get('product')
                    result = str(result).split('-')
                    # quantity = request.COOKIES.get('quantity')
                    # quantity = str(quantity).split('-')
                    for name in result:
                        product = Product.objects.get(name=name)
                        cost += product.price
                        product_list.append(product.name)
                    request.session['order'] = product_list
            request.session['cost'] = str(cost)
            return redirect('reservation')
        # elif "remove" in request.POST:
        #     pt_remove = request.POST['remove']
        #     stop = 0
        #     result = request.COOKIES.get('product')
        #     for pt in result:
        #         if pt_remove == pt:
        #             pass
        else:
            return redirect('home')
        
class ReservationView(View):
    def get(self, request):
        context = {
            'total': request.session['cost']
        }
        return render(request, "customer/reserve.html", context)
    
    def post(self, request):
        cost = request.session['cost']
        del request.session['cost']
        table = request.POST['subject']
        date = request.POST['date']
        time = request.POST['time']
        email = request.POST['2email']
        phone_number = request.POST['tel']
        if table == '1':
            table = "2 person"
        elif table == '2':
            table = "5 person"
        elif table == '3':
            table = "6 person"

        reserve_info = {
            'table': table,
            'date': date,
            'time': time,
            'email': email,
            'cost': cost,
            'phone_number': phone_number
        }
        request.session['reserve'] = reserve_info
        return redirect('home')