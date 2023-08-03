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
                    if request.COOKIES.get('product'):
                        product1 = request.COOKIES.get('product')
                        product1 += f"-{result}"  #produc1 = farzad-nima-mmd-sina
                        cat = category()
                        product = Product.objects.all()
                        context = {
                            "category": cat,
                            "product": product
                        }
                        res = render(request, 'menu/menu.html', context)
                        res.set_cookie('product', product1)
                        return res
                        # res = render(request, 'menu/menu.html', context)
                        # res.delete_cookie('product')
                        # return res
                    else:
                        cat = category()
                        product = Product.objects.all()
                        context = {
                            "category": cat,
                            "product": product
                        }
                        response = render(request, 'menu/menu.html')
                        response.set_cookie(key='product', value=result)
                        return response
    else:
        cat = category()
        product = Product.objects.all()
        context = {
            "category": cat,
            "product": product
        }
        return render(request,"menu/menu.html", context)
