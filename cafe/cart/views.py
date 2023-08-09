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
        
