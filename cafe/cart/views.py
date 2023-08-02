from django.shortcuts import render, get_object_or_404
from menu.models import Product
# Create your views here.
def cart_page(request):
    result = request.session['product']
    pt = list()
    for name in result:
        product = Product.objects.get(name=name)
        pt.append(product)

    context = {
        'product': pt
    }
    return render(request, "cart/cart.html", context)