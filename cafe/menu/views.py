from django.shortcuts import render, HttpResponse, redirect
from category.views import category
from . models import Product

# Create your views here.
def menu_page(request):
    if request.method == "POST":
        if 'all' in request.POST:
            cat = category()
            product = Product.objects.all()
            context = {
            "category": cat,
            "product": product
            }
            return render(request,"menu/menu.html", context)
        else:
            cat = category()
            product = Product.objects.all()
            for cat_obj in cat:
                if cat_obj.name in request.POST:
                    product_cat = Product.objects.filter(category_menu=cat_obj)
                    context = {
                        "category": cat,
                        "product": product_cat
                    }
                    return render(request, 'menu/menu.html', context)
            for pt in product:
                if pt.name in request.POST:
                    result = pt.name
                    # del request.session['product']
                    if request.session.has_key('product'):
                        product = request.session['product']
                        product.append(result)
                        request.session['product'] = product
                    else:
                        request.session['product'] = [result,]
                    return redirect('menu')
    else:
        cat = category()
        product = Product.objects.all()
        context = {
            "category": cat,
            "product": product
        }
        return render(request,"menu/menu.html", context)
