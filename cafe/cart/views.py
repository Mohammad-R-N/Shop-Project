from django.shortcuts import render, redirect
from menu.models import Product

# Create your views here.
def cart_page(request):
    if request.method == "GET":
        if request.COOKIES.get('product') is not None:
            result = request.COOKIES.get('product')
            result = str(result).split('-')
            pt = list()
            for name in result:
                product = Product.objects.get(name=name)
                pt.append(product)
            context = {
                'product': pt
            }
            return render(request, "cart/cart.html", context)
        else:
            return render(request, "cart/cart.html")
    if request.method == "POST":
        if "done" in request.POST:
            pt2 = list()
            if request.COOKIES.get('product') is not None:
                result = request.COOKIES.get('product')
                result = str(result).split('-')
                for name in result:
                    product = Product.objects.get(name=name)
                    pt2.append(product)
            request.session['order'] = pt2
            return redirect('menu')
        else:
            return redirect('home')