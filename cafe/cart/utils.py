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
        
        return new_cookie

    def accept_shop_cart(request):
        if request.COOKIES.get('product') is not None:
            if len(request.COOKIES.get('product')) > 1:
                result = request.COOKIES.get('product')
                result = str(result).split('-')
                result.pop(0)
                request.session['order'] = result
                request.session['cost'] = request.session['total']
                del request.session['total']
                return True
            else:
                return False

class Reservation:
    def checkout(request, product_m, table_m, cart_m, orderItem_m):
        cost = request.session['cost']
        del request.session['cost']

        order = request.session['order']
        del request.session['order']

        table = request.POST['subject']
        phone_number = request.POST['tel']

        table_obj = table_m.objects.get(table_name=table)          
        cart = cart_m.objects.create(total_price=cost, total_quantity=len(order), 
                                    customer_number=phone_number, cart_table=table_obj)
        cart.save()

        for ord in order:
            pt_name = ord.split('=')
            pt = product_m.objects.get(name=pt_name[0])
            order_item = orderItem_m.objects.create(product=pt, cart=cart, quantity=pt_name[1], price=pt.price)
            order_item.save()

        return phone_number

class OrderDetail:
    def show_cart_detail(request, cart_m, orderItem_m):
        phone_number = request.COOKIES.get('number')
        cart = cart_m.objects.all()
        item = list()
        cart_list = list()
        status = list()
        for cart_obj in cart:
            if cart_obj.customer_number == phone_number:
                items = orderItem_m.objects.filter(cart=cart_obj)
                cart_list.append(cart_obj)

                item.append(items[0])
                if cart_obj.status == "w":
                    status.append("Waiting for accept from Admin")
                elif cart_obj.status == "a":
                    status.append("Accepted from Admin")
                elif cart_obj.status == "r":
                    status.append("Refused from Admin")
        return item, cart_list, status
