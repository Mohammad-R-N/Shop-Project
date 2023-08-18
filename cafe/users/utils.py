from cart.models import OrderItem, Cart, Table
from django.contrib import messages

class StaffPanel:
    def waiting_post(model):
        cart = model.objects.all()
        item = list()
        carts = list()

        for cart_obj in cart:
            if cart_obj.status == "w":
                items = OrderItem.objects.filter(cart=cart_obj)
                item.append(items[0])
                carts.append(cart_obj)
        return item, carts
    
    def accept_ord(request):
        if "accepted_ord" in request.POST:
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "a":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items)
                    carts.append(cart_obj)
            return item, carts
        
    def refuse_ord(request):
        if "refused_ord" in request.POST:
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "a":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items)
                    carts.append(cart_obj)
            return item, carts
        
    def get_ord_by_phone(request):
        phone = request.POST["phone_number"]
        cart = Cart.objects.all()
        item_list = list()
        cart_list = list()

        for cart_obj in cart:
            if cart_obj.customer_number == phone:
                item = OrderItem.objects.filter(cart=cart_obj)
                item_list.append(item[0])
                cart_list.append(cart_obj)
        return item_list, cart_list
        
    def make_refuse(request, model):
        user = request.user
        cart_refuse_id = request.POST["refuse"]
        cart = model.objects.all()

        for cart_obj in cart:
            if cart_obj.id == int(cart_refuse_id):
                update_cart = model.objects.get(id=cart_obj.id)
                update_cart.status = "r"
                update_cart.cart_users = user
                update_cart.save()
                messages.success(request, "Refused successfully!", "warning")
        return None
    
    def make_accept(request, model):
        user = request.user
        cart_accept_id = request.POST["accept"]
        cart = model.objects.all()

        for cart_obj in cart:
            if cart_obj.id == int(cart_accept_id):
                update_cart = model.objects.get(id=cart_obj.id)
                update_cart.status = "a"
                update_cart.cart_users = user
                update_cart.save()
                messages.success(request, "Accepted successfully!", "success")
        return None
    
    def get_ord_for_edit(request, model):
        cart_edit_id = request.session["edit_id"]
        cart = model.objects.all()
        item = list()
        cart_list = list()

        for cart_obj in cart:
            if cart_obj.id == int(cart_edit_id):
                items = OrderItem.objects.filter(cart=cart_obj)
                cart_list.append(cart_obj)
                item.append(items)
        return item, cart_list[0].customer_number

    def remove_ord(request, model):
        cart_edit_id = request.session["edit_id"]
        order_item_id = request.POST["remove"]
        cart = model.objects.all()
        item_list = list()

        for cart_obj in cart:
            if cart_obj.id == int(cart_edit_id):
                items = OrderItem.objects.filter(cart=cart_obj)
                item_list.append(items[0])

        for item in item_list:
            if item.id == int(order_item_id):
                OrderItem.objects.get(id=int(order_item_id)).delete()
                messages.success(request, "Deleted successfully!", "warning")
                return True
        return False
    
    def save_new_quantity(request, model):
        order_items = model.objects.all()

        for ord in order_items:
            if str(ord.id) in request.POST:
                new_quantity = request.POST[f"{ord.id}"]
                old_quantity = ord.quantity
                total_quantity = int(old_quantity) - int(new_quantity)
                ord.quantity = int(new_quantity)
                ord.cart.total_price = ord.price * int(new_quantity)
                ord.cart.total_quantity = abs(total_quantity)
                ord.save()
                return True
        return False
    
    
