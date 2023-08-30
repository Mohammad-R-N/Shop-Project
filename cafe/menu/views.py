from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from . models import Product
from . models import Category
from django.views import View
from django.db.models import Q

# Create your views here.
class MenuView(View):
    def get(self, request):
        cat = Category.objects.all()
        product = Product.objects.all()
        context = {"category": cat, "product": product}
        return render(request,"menu/menu.html", context)
    
    def post(self, request):
        if 'all' in request.POST:
            cat = Category.objects.all()
            product = Product.objects.all()
            context = {"category": cat, "product": product}
            return render(request, "menu/menu.html", context)
        else:
            cat = Category.objects.all()
            product = Product.objects.all()
            for cat_obj in cat:
                if cat_obj.name in request.POST:
                    product_cat = Product.objects.filter(category_menu=cat_obj)
                    context = {"category": cat, "product": product_cat}
                    return render(request, "menu/menu.html", context)
            for pt in product:
                if pt.name in request.POST:
                    quantity = request.POST['quantity']
                    result = pt.name
                    if request.COOKIES.get('product'):
                        product_cookie = request.COOKIES.get('product')
                        product_cookie += f"-{result}={quantity}"  #product_cookie = latte=2-product=4
                        cat = Category.objects.all()
                        product = Product.objects.all()
                        context = {"category": cat, "product": product}
                        res = render(request, "menu/menu.html", context)
                        res.set_cookie("product", product_cookie)
                        # res.delete_cookie("product")
                        return res

                    else:
                        cat = Category.objects.all()
                        product = Product.objects.all()

                        context = {
                            "category": cat,
                            "product": product
                        }
                        response = render(request, 'menu/menu.html', context)
                        response.set_cookie(key='product', value=f"-{result}={quantity}")
                        return response

class SearchProducts(View):
    def get(self, request):
        query = request.GET.get(
            "query", ""
        ).strip()
        if not query:
            results = []
        else:
            results = Product.objects.filter( Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query))
        return render(
            request, "menu/search_results.html", {"results": results, "query": query}
        )
    
class ProductPopup(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, "menu/product_detail.html", {"product": product})