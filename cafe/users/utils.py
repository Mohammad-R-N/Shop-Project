from cart.models import OrderItem, Cart, Table
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

class StaffPanel:

    @staticmethod
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
    @staticmethod
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

    @staticmethod    
    def refuse_ord(request):
        if "refused_ord" in request.POST:
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "r":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items)
                    carts.append(cart_obj)
            return item, carts

    @staticmethod    
    def get_ord_by_table(request):
        table_number = request.POST["table"]
        table_obj = Table.objects.get(table_name=table_number)
        cart = Cart.objects.all()
        item_list = list()
        cart_list = list()

        for cart_obj in cart:
            if cart_obj.cart_table == table_obj and cart_obj.status == "w":
                item = OrderItem.objects.filter(cart=cart_obj)
                item_list.append(item[0])
                cart_list.append(cart_obj)
        return item_list, cart_list, f'Search result for table "{table_number}"'

    @staticmethod  
    def get_ord_by_date(request):
        date = request.POST["date"]
        cart = Cart.objects.all()
        item_list = list()
        cart_list = list()

        for cart_obj in cart:
            if str(cart_obj.time.date()) == date and cart_obj.status == "w":
                item = OrderItem.objects.filter(cart=cart_obj)
                item_list.append(item[0])
                cart_list.append(cart_obj)
        return item_list, cart_list, f'Search result for "{date}"'
    

    @staticmethod   
    def get_ord_by_phone(request):
        phone = request.POST["phone_number"]
        cart = Cart.objects.all()
        item_list = list()
        cart_list = list()

        for cart_obj in cart:
            if cart_obj.customer_number == phone and cart_obj.status == "w":
                item = OrderItem.objects.filter(cart=cart_obj)
                item_list.append(item[0])
                cart_list.append(cart_obj)
        return item_list, cart_list, f'Search result for "{phone}"'

    @staticmethod    
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
                # messages.success(request, "Refused successfully!", "warning")
        return None
    
    @staticmethod
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
                # messages.success(request, "Accepted successfully!", "success")
        return None

class StaffEditOrd:
    @staticmethod
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

    @staticmethod
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
                # messages.success(request, "Deleted successfully!", "warning")
                return True
        return False
    
    @staticmethod
    def save_new_quantity(request, model):
        order_items = model.objects.all()

        for ord in order_items:
            if str(ord.id) in request.POST:
                new_quantity = request.POST[f"{ord.id}"]
                if new_quantity == "":
                    return True
                else:
                    old_quantity = ord.quantity
                    total_quantity = int(old_quantity) - int(new_quantity)
                    ord.quantity = int(new_quantity)
                    ord.cart.total_price = ord.price * int(new_quantity)
                    ord.cart.total_quantity = abs(total_quantity)
                    ord.save()
                    return True
        return False

class StaffAddOrd:
    @staticmethod
    def show_product_in_cat(request, model, category_m):
        cat = category_m.objects.all()
        product = model.objects.all()
        for cat_obj in cat:
            if cat_obj.name in request.POST:
                product_cat = model.objects.filter(category_menu=cat_obj)
        return cat, product_cat

    @staticmethod
    def add_ord_to_shop_cart(request, model):
        cart_edit_id = request.session["edit_id"]
        new_product_id = request.POST["add"]
        new_product_quantity = request.POST["quantity"]
        new_product_obj = model.objects.get(id=int(new_product_id))
        cart = Cart.objects.all()

        for cart_obj in cart:
            if cart_obj.id == int(cart_edit_id):
                order_item = OrderItem.objects.create(
                    product=new_product_obj,
                    cart=cart_obj,
                    quantity=int(new_product_quantity),
                    price=new_product_obj.price,
                )
                order_item.save()
                cart_obj.total_price = cart_obj.total_price + int(
                    new_product_obj.price
                ) * int(new_product_quantity)
                cart_obj.total_quantity += 1
                cart_obj.save()
                return True
        return False
    
class ExportCsv:

    @staticmethod
    def generate_csv_response(data, header, filename):
        csv_content = ",".join(header) + "\n"
        for row in data:
            csv_content += ",".join(map(str, row)) + "\n"

        response = HttpResponse(csv_content, content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
        return response

class Customer:

    @staticmethod
    def get_ord_by_phone(request, model):
        number = request.POST["tel"]
        cart = model.objects.all()
        item_list = list()
        cart_list = list()

        for cart_obj in cart:
            if cart_obj.customer_number == number:
                item = OrderItem.objects.filter(cart=cart_obj).values()
                item_list.append(item)
                cart_list.append(cart_obj)
        return item_list, cart_list

class Manager:

    @staticmethod
    def status_count(request, today, model):
        accepted_carts_count = model.objects.filter(
            status=model.ACCEPT, time__date=today
        ).count()
        refused_carts_count = model.objects.filter(
            status=model.REFUSE, time__date=today
        ).count()
        total_carts_count = accepted_carts_count + refused_carts_count

        if total_carts_count == 0:
            accepted_percentage = 0
            refused_percentage = 0
        else:
            accepted_percentage = (accepted_carts_count / total_carts_count) * 100
            refused_percentage = (refused_carts_count / total_carts_count) * 100

        data = {
            "accepted_count": accepted_carts_count,
            "refused_count": refused_carts_count,
            "accepted_percentage": accepted_percentage,
            "refused_percentage": refused_percentage,
        }

        if request.GET.get("format") == "csv":
            csv_content = "Status, Count, Percentage\n"
            csv_content += (
                f"Accepted,{accepted_carts_count},{accepted_percentage:.2f}%\n"
            )
            csv_content += f"Refused,{refused_carts_count},{refused_percentage:.2f}%\n"

            response = HttpResponse(csv_content, content_type="text/csv")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="status_count_report.csv"'
            return response
        return data

    @staticmethod
    def status_order(request, today, model):
        accepted_carts_count = model.objects.filter(
            status=model.ACCEPT, time__date=today
        ).count()
        refused_carts_count = model.objects.filter(
            status=model.REFUSE, time__date=today
        ).count()
        waiting_carts_count = model.objects.filter(
            status=model.WAITING, time__date=today
        ).count()

        data = {
            "accepted_count": accepted_carts_count,
            "refused_count": refused_carts_count,
            "waiting_count": waiting_carts_count,
        }

        if request.GET.get("format") == "csv":
            csv_content = "Order Status, Count\n"
            csv_content += f"Accepted,{accepted_carts_count}\n"
            csv_content += f"Refused,{refused_carts_count}\n"
            csv_content += f"Waiting,{waiting_carts_count}\n"

            response = HttpResponse(csv_content, content_type="text/csv")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="order_status_report.csv"'
            return response
        return data

