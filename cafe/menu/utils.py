from django.db.models import Q

class MenuOption:
    def get_menu_objects(category_m, product_m):
        cat = category_m.objects.all()
        product = product_m.objects.all()
        return cat, product
    
    def get_product_by_category(category_obj, product_m):
        product_cat = product_m.objects.filter(category_menu=category_obj)
        return product_cat

    def search_product(request, product_m):
        query = request.GET.get("query", "").strip()

        if not query:
            results = []
        else:
            results = product_m.objects.filter( Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query))
        
        return query, results