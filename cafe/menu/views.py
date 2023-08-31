from django.shortcuts import render
from . models import Product
from . models import Category
from django.views import View
from .utils import MenuOption

# Create your views here.
class MenuView(View):
    def get(self, request):
        result = MenuOption.get_menu_objects(Category, Product)
        context = {"category": result[0], "product": result[1]}
        return render(request,"menu/menu.html", context)
    
    def post(self, request):
        if 'all' in request.POST:
            result = MenuOption.get_menu_objects(Category, Product)
            context = {"category": result[0], "product": result[1]}
            return render(request, "menu/menu.html", context)
        else:
            result = MenuOption.get_menu_objects(Category, Product)
            for cat_obj in result[0]:
                if cat_obj.name in request.POST:
                    product_by_cat = MenuOption.get_product_by_category(cat_obj, Product)
                    context = {"category": result[0], "product": product_by_cat}
                    return render(request, "menu/menu.html", context)
                
            for pt in result[1]:
                if pt.name in request.POST:
                    quantity = request.POST['quantity']
                    product_name = pt.name
                    if request.COOKIES.get('product'):
                        product_cookie = request.COOKIES.get('product')
                        product_cookie += f"-{product_name}={quantity}"  #product_cookie = latte=2-product=4
                        result = MenuOption.get_menu_objects(Category, Product)
                        context = {"category": result[0], "product": result[1]}
                        res = render(request, "menu/menu.html", context)
                        res.set_cookie("product", product_cookie)
                        # res.delete_cookie("product")
                        return res

                    else:
                        result = MenuOption.get_menu_objects(Category, Product)
                        context = {"category": result[0], "product": result[1]}
                        response = render(request, 'menu/menu.html', context)
                        response.set_cookie(key='product', value=f"-{product_name}={quantity}")
                        return response

class SearchProducts(View):
    def get(self, request):
        result = MenuOption.search_product(request, Product)
        return render(request, "menu/search_results.html", {"results": result[1], "query": result[0]})
    
class ProductPopup(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, "menu/product_detail.html", {"product": product})