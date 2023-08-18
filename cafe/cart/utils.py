from django.shortcuts import redirect

class ProductOption:
    def show_product(request, model):
        cost = 0
        product_list = list()
        result = request.COOKIES.get('product')
        result = str(result).split('-')
        result.pop(0)
        
        for name in result:
            pt_name = name.split('=')
            product = model.objects.get(name=pt_name[0])
            data = dict()
            data['product_name'] = product.name
            data['product_photo'] = product.photo.url
            data['product_price'] = product.price
            data['product_quantity'] = pt_name[1]
            data['total'] = int(pt_name[1]) * product.price
            product_list.append(data)

        for pt in product_list:
            cost += pt['total']
        
        request.session['total'] = str(cost)

        return cost, product_list

    def remove_from_shop_cart(request):
        remove = request.POST['remove']
        result = request.COOKIES.get('product')
        result = str(result).split('-')
        result.pop(0)
        new_cookie = ''

        for name in result:
            pt_name = name.split('=')
            if pt_name[0] == remove:
                pass
            else:
                new_cookie += f"-{pt_name[0]}={pt_name[1]}"
        try:
            response = redirect("cart")
            response.set_cookie(key='product', value=new_cookie)
            return response
        except:
            response = redirect("cart")
            response.set_cookie(key='product', value='')
            return response

    def accept_shop_cart(request):
        if request.COOKIES.get('product') is not None:
            if len(request.COOKIES.get('product')) > 1:
                result = request.COOKIES.get('product')
                result = str(result).split('-')
                result.pop(0)
                request.session['order'] = result
                request.session['cost'] = request.session['total']
                del request.session['total']
                return redirect('reservation')
            else:
                return redirect('cart')




