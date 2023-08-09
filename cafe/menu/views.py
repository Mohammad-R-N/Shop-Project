
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from . models import Product
from . models import Category
from django.views import View

# Create your views here.
class MenuView(View):
    def get(self, request):
        cat = Category.objects.all()
        product = Product.objects.all()
        context = {
            "category": cat,
            "product": product
        }
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
                    result = pt.name

                    if request.COOKIES.get('product'):
                        product1 = request.COOKIES.get('product')
                        product1 += f"-{result}"  #produc1 = farzad-nima-mmd-sina
                        cat = Category.objects.all()

                        product = Product.objects.all()
                        context = {"category": cat, "product": product}
                        res = render(request, "menu/menu.html", context)
                        res.set_cookie("product", product1)
                        return res
                        # res = render(request, 'menu/menu.html', context)
                        # res.delete_cookie('product')
                        # return res
                    # elif request.COOKIES.get('quantity'):
                    #     quantity = request.COOKIES.get('quantity')
                    #     quantity += f"-{res_quantity}"
                    #     cat = Category.objects.all()
                    #     product = Product.objects.all()
                    #     context = {
                    #         "category": cat,
                    #         "product": product
                    #     }
                    #     res = render(request, 'menu/menu.html', context)
                    #     res.set_cookie('quantity', quantity)
                    #     return res
                    else:
                        cat = Category.objects.all()
                        product = Product.objects.all()

                        context = {
                            "category": cat,
                            "product": product
                        }
                        response = render(request, 'menu/menu.html')
                        response.set_cookie(key='product', value=result)
                        # response.set_cookie(key='quantity', value=res_quantity)
                        return response


def search_products(request):
    query = request.GET.get(
        "query", ""
    ).strip()  # Using 'query' and stripping whitespace
    if not query:  # If the query is empty
        results = []
    else:
        results = Product.objects.filter(name__icontains=query)
    return render(
        request, "menu/search_results.html", {"results": results, "query": query}
    )

class ProductPopup(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, "menu/product_detail.html", {"product": product})