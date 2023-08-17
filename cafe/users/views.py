from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import StaffLoginForm, StaffOtpForm
from django.views import View
from cart.models import OrderItem
import random
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.db.models.functions import (
    ExtractWeekDay,
    ExtractMonth,
    ExtractYear,
    ExtractHour,
)


# from utils import send_OTP
from .models import CustomUser
from menu.models import Product, Category
from cart.models import Cart, OrderItem
from .authentication import CustomAuthBackend
import re
from django.db.models import Sum, Count
from django.utils import timezone
from django.contrib import messages


class StaffLogin(View):
    form_staff = StaffLoginForm

    def get(self, request):
        form = self.form_staff
        return render(request, "staff/login.html", {"form": form})

    def post(self, request):
        form = self.form_staff(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            print(random_code)
            CustomUser.objects.update(code=random_code)
            phone_number = form.cleaned_data.get("phone_number")
            formatted_phone_number = re.sub(r"^\+98|^0098", "0", phone_number)

            user = CustomUser.objects.filter(
                phone_number=formatted_phone_number
            ).first()
            if user is None:
                messages.error(request, "User not found!", "danger")
                return redirect(
                    "login"
                )  # Redirect to signup page if user is not registered
            else:
                send_OTP(formatted_phone_number, random_code)
                request.session["user_info"] = {
                    "phone_number": formatted_phone_number,
                    "code": random_code,
                }
                return redirect("check-otp")

            # class CheckOtp(View):
            #     form_otp = StaffOtpForm

            #     def get(self, request):
            #         form = self.form_otp()
            #         return render(request, "staff/otp.html", {"form": form})

            #     def post(self, request):
            #         form = self.form_otp(request.POST)
            #         if form.is_valid():
            #             otp = form.cleaned_data["code"]
            #             user = CustomAuthBackend.authenticate(request, phone_number=request.session["user_info"]["phone_number"], code=otp)

            #             if user is not None:
            #                 login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            #                 return redirect("staff")
            #             return redirect("home")
            #         return redirect('menu')

            if user is not None:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                messages.success(request, "Loged In Successfully", "success")
                return redirect("staff")
            messages.error(request, "OTP code is NOT CORRECT!", "danger")
            return redirect("home")
        return redirect("menu")


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "LogOut Successfully!", "success")
        return redirect("home")


class StaffPanelView(View):
    template_staff = "staff/staff.html"
    # template_staff_login = "staff/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # return redirect("staff_login")
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "w":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items)
                    carts.append(cart_obj)

            context = {"item": item, "cart": carts}
            return render(request, self.template_staff, context)
        else:
            messages.error(
                request, "You are NOT allowed to see staff panel", extra_tags="danger"
            )
            return render(request, "staff_login")

    def post(self, request):
        if "refuse" in request.POST:
            cart_refuse_id = request.POST["refuse"]
            cart = Cart.objects.all()

            for cart_obj in cart:
                if cart_obj.id == int(cart_refuse_id):
                    update_cart = Cart.objects.get(id=cart_obj.id)
                    update_cart.status = "r"
                    update_cart.save()
                    messages.success(request, "Refused successfully!", "warning")
            return redirect("staff")

        elif "accept" in request.POST:
            cart_accept_id = request.POST["accept"]
            cart = Cart.objects.all()

            for cart_obj in cart:
                if cart_obj.id == int(cart_accept_id):
                    update_cart = Cart.objects.get(id=cart_obj.id)
                    update_cart.status = "a"
                    update_cart.save()
                    messages.success(request, "Accepted successfully!", "success")
            return redirect("staff")

        elif "edit" in request.POST:
            cart_edit_id = request.POST["edit"]
            request.session["edit_id"] = cart_edit_id
            return redirect("edit_ord")


class EditOrder(View):
    template_name = "staff/edit_ord.html"

    def get(self, request):
        if request.session.has_key("edit_id"):
            cart_edit_id = request.session["edit_id"]
            cart = Cart.objects.all()
            item = list()
            cart_list = list()

            for cart_obj in cart:
                if cart_obj.id == int(cart_edit_id):
                    items = OrderItem.objects.filter(cart=cart_obj).values()
                    # print(items[1]['product_id'])
                    cart_list.append(cart_obj)
                    item.append(items)

            context = {
                "cart": cart_list[0].customer_number,
                "items": item,
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name)

    def post(self, request):
        if "remove" in request.POST:
            cart_edit_id = request.session["edit_id"]
            order_item_id = request.POST["remove"]
            cart = Cart.objects.all()
            item_list = list()

            for cart_obj in cart:
                if cart_obj.id == int(cart_edit_id):
                    items = OrderItem.objects.get(cart=cart_obj)
                    item_list.append(items)

            for item in item_list:
                if item.id == int(order_item_id):
                    OrderItem.objects.get(id=int(order_item_id)).delete()
                    messages.success(request, "Deleted successfully!", "warning")
                    return redirect("staff")

        elif "done" in request.POST:
            order_items = OrderItem.objects.all()

            for ord in order_items:
                if str(ord.id) in request.POST:
                    new_quantity = request.POST[f"{ord.id}"]
                    ord.quantity = int(new_quantity)
                    ord.cart.total_price = ord.price * int(new_quantity)
                    ord.save()
                    return redirect("staff")

        elif "add_ord" in request.POST:
            return redirect("add_ord")


class AddOrder(View):
    template_name = "staff/staff_add_order.html"

    def get(self, request):
        cat = Category.objects.all()
        product = Product.objects.all()
        context = {"category": cat, "product": product}
        return render(request, self.template_name, context)

    def post(self, request):
        if "add" in request.POST:
            cart_edit_id = request.session["edit_id"]
            new_product_id = request.POST["add"]
            new_product_quantity = request.POST["quantity"]
            new_product_obj = Product.objects.get(id=int(new_product_id))
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

        elif "all" in request.POST:
            cat = Category.objects.all()
            product = Product.objects.all()
            context = {"category": cat, "product": product}
            return render(request, self.template_name, context)
        else:
            cat = Category.objects.all()
            product = Product.objects.all()
            for cat_obj in cat:
                if cat_obj.name in request.POST:
                    product_cat = Product.objects.filter(category_menu=cat_obj)
                    context = {"category": cat, "product": product_cat}
                    return render(request, self.template_name, context)


class PopularItemsView(ListView):
    model = OrderItem

    def get_queryset(self):
        return (
            OrderItem.objects.values("product__name")
            .annotate(total_ordered=Sum("quantity"))
            .order_by("-total_ordered")[:5]
        )

    def render_to_response(self, context, **response_kwargs):
        items = context["object_list"]
        product_names = [item["product__name"] for item in items]
        quantities = [item["total_ordered"] for item in items]

        return JsonResponse({"product_names": product_names, "quantities": quantities})


class SalesByCustomerView(ListView):
    model = Cart

    def get_queryset(self):
        return (
            Cart.objects.values("customer_number")
            .annotate(total_sales=Sum("total_price"))
            .order_by("-total_sales")[:3]
        )

    def render_to_response(self, context, **response_kwargs):
        sales = context["object_list"]
        customer_numbers = [sale["customer_number"] for sale in sales]
        total_sales = [sale["total_sales"] for sale in sales]

        return JsonResponse(
            {"customer_numbers": customer_numbers, "total_sales": total_sales}
        )


class PeakBusinessHourView(ListView):
    model = Cart

    def get_queryset(self):
        return (
            Cart.objects.annotate(hour=ExtractHour("time"))
            .values("hour")
            .annotate(order_count=Count("id"))
            .order_by("-order_count")[:6]
        )

    def render_to_response(self, context, **response_kwargs):
        hours = context["object_list"]
        peak_hour = hours[:6] if hours else None
        return JsonResponse({"peak_hour": peak_hour})


class SalesByCategoryView(ListView):
    model = OrderItem

    def get_queryset(self):
        return (
            OrderItem.objects.select_related("product")
            .values("product__category_menu__name")
            .annotate(total_sales=Sum("price"))
            .order_by("-total_sales")
        )

    def render_to_response(self, context, **response_kwargs):
        categories = context["object_list"]
        category_names = [
            category["product__category_menu__name"] for category in categories
        ]
        total_sales = [category["total_sales"] for category in categories]
        return JsonResponse(
            {"category_names": category_names, "total_sales": total_sales}
        )


class SalesByEmployeeView(ListView):
    model = Cart

    def get_queryset(self):
        return (
            Cart.objects.values("cart_users__phone_number")
            .annotate(total_sales=Sum("total_price"))
            .order_by("-total_sales")[:3]
        )

    def render_to_response(self, context, **response_kwargs):
        sales = context["object_list"]
        phone_numbers = [sale["cart_users__phone_number"] for sale in sales]
        total_sales = [sale["total_sales"] for sale in sales]
        return JsonResponse(
            {
                "phone_numbers": phone_numbers,
                "total_sales": total_sales,
            }
        )


class CustomerHistory(View):
    template_login = "manager/history_login_manager.html"
    template_history = "manager/history_for_manager.html"

    def get(self, request):
        return render(request, self.template_login)

    def post(self, request):
        if "tel" in request.POST:
            number = request.POST["tel"]
            cart = Cart.objects.all()
            item_list = list()
            cart_list = list()

            for cart_obj in cart:
                if cart_obj.customer_number == number:
                    item = OrderItem.objects.filter(cart=cart_obj).values()
                    item_list.append(item)
                    cart_list.append(cart_obj)
            print(item_list)
            context = {"items": item_list, "carts": cart_list}
            return render(request, self.template_history, context)
        else:
            return render(request, self.template_history)


class PopularItemsMorningView(ListView):
    model = OrderItem

    def get_queryset(self):
        start_time = timezone.datetime.now().replace(
            hour=8, minute=0, second=0, microsecond=0
        )
        end_time = timezone.datetime.now().replace(
            hour=12, minute=0, second=0, microsecond=0
        )
        return (
            OrderItem.objects.filter(cart__time__range=(start_time, end_time))
            .values("product__name")
            .annotate(total_ordered=Sum("quantity"))
            .order_by("-total_ordered")[:2]
        )

    def render_to_response(self, context, **response_kwargs):
        items = context["object_list"]
        product_names = [item["product__name"] for item in items]
        quantities = [item["total_ordered"] for item in items]
        return JsonResponse({"product_names": product_names, "quantities": quantities})


class StatusCountView(View):
    def get(self, request):
        today = timezone.now().today().date()
        accepted_carts_count = Cart.objects.filter(status="a", time=today).count()
        refused_carts_count = Cart.objects.filter(status="r", time=today).count()
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

        return JsonResponse(data)


class OrderStatusReportView(View):
    def get(self, request):
        today = timezone.now().today().date()

        accepted_carts_count = Cart.objects.filter(
            status=Cart.ACCEPT, time__date=today
        ).count()
        refused_carts_count = Cart.objects.filter(
            status=Cart.REFUSE, time__date=today
        ).count()
        waiting_carts_count = Cart.objects.filter(
            status=Cart.WAITING, time__date=today
        ).count()

        data = {
            "accepted_count": accepted_carts_count,
            "refused_count": refused_carts_count,
            "waiting_count": waiting_carts_count,
        }

        return JsonResponse(data)


class TopSellingItemsView(ListView):
    model = OrderItem

    def get_queryset(self):
        date_filter = self.request.GET.get("date", timezone.now().date())

        return (
            OrderItem.objects.filter(cart__time__date=date_filter)
            .values("product__name")
            .annotate(total_ordered=Sum("quantity"))
            .order_by("-total_ordered")
        )

    def render_to_response(self, context, **response_kwargs):
        items = context["object_list"]
        product_names = [item["product__name"] for item in items]
        quantities = [item["total_ordered"] for item in items]

        data = {"product_names": product_names, "quantities": quantities}

        return JsonResponse(data)
