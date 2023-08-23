class CustomerOption:
    def show_customer_history(request, cart_m, orderItem_m):
        number = request.COOKIES.get('number')
        cart = cart_m.objects.all()
        item_list = list()
        cart_list = list()

        for cart_obj in cart:
            if cart_obj.customer_number == number:
                item = orderItem_m.objects.filter(cart=cart_obj)
                item_list.append(item[0])
                cart_list.append(cart_obj)
        return item_list, cart_list





