from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import StaffLoginForm, StaffOtpForm
from django.views import View
from cart.models import OrderItem
import random
from django.http import JsonResponse, HttpResponse
from django.views.generic.list import ListView
from django.db.models.functions import (
    ExtractWeekDay,
    ExtractMonth,
    ExtractYear,
    ExtractHour,
)


from utils import send_OTP
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
                    "staff_login"
                )  # Redirect to signup page if user is not registered
            else:
                send_OTP(formatted_phone_number, random_code)
                request.session["user_info"] = {
                    "phone_number": formatted_phone_number,
                    "code": random_code,
                }
                return redirect("check-otp")


class CheckOtp(View):
    form_otp = StaffOtpForm

    def get(self, request):
        form = self.form_otp()
        return render(request, "staff/otp.html", {"form": form})

    def post(self, request):
        form = self.form_otp(request.POST)
        if form.is_valid():
            otp = form.cleaned_data["code"]
            user = CustomAuthBackend.authenticate(
                request,
                phone_number=request.session["user_info"]["phone_number"],
                code=otp,
            )
            if user is not None:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                messages.success(request, "Loged In Successfully", "success")
                return redirect("staff")

            messages.error(request, "OTP code is NOT CORRECT!", "danger")
            return redirect("staff_login")
        return redirect("menu")


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "LogOut Successfully!", "success")
        return redirect("staff_login")


class StaffPanelView(View):
    template_staff = "staff/staff.html"
    template_staff_login = "staff/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "w":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items[0])
                    carts.append(cart_obj)

            context = {"item": item, "cart": carts}
            return render(request, self.template_staff, context)
        else:
            messages.error(
                request, "You are NOT allowed to see staff panel", extra_tags="danger"
            )
            return redirect("staff_login")

    def post(self, request):
        user = request.user

        if "accepted_ord" in request.POST:
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "a":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items)
                    carts.append(cart_obj)

            context = {"item": item, "cart": carts}
            return render(request, "staff/staff_accepted.html", context)

        elif "refused_ord" in request.POST:
            cart = Cart.objects.all()
            item = list()
            carts = list()

            for cart_obj in cart:
                if cart_obj.status == "r":
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item.append(items)
                    carts.append(cart_obj)

            context = {"item": item, "cart": carts}
            return render(request, "staff/staff_refused.html", context)

        elif "waiting_ord" in request.POST:
            return redirect("staff")

        elif "phone_number" in request.POST:
            phone = request.POST["phone_number"]

            cart = Cart.objects.all()
            item_list = list()
            cart_list = list()

            for cart_obj in cart:
                if cart_obj.customer_number == phone:
                    item = OrderItem.objects.filter(cart=cart_obj)
                    item_list.append(item[0])
                    cart_list.append(cart_obj)

            context = {"items": item_list, "carts": cart_list}
            return render(request, "staff/staff_search_result.html", context)

        elif "refuse" in request.POST:
            cart_refuse_id = request.POST["refuse"]
            cart = Cart.objects.all()

            for cart_obj in cart:
                if cart_obj.id == int(cart_refuse_id):
                    update_cart = Cart.objects.get(id=cart_obj.id)
                    update_cart.status = "r"
                    update_cart.cart_users = user
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
                    update_cart.cart_users = user
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
                    items = OrderItem.objects.filter(cart=cart_obj)
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
                    items = OrderItem.objects.filter(cart=cart_obj)
                    item_list.append(items[0])

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
                    old_quantity = ord.quantity
                    total_quantity = int(old_quantity) - int(new_quantity)
                    ord.quantity = int(new_quantity)
                    ord.cart.total_price = ord.price * int(new_quantity)
                    ord.cart.total_quantity = abs(total_quantity)
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
                    cart_obj.total_price = cart_obj.total_price + int(
                        new_product_obj.price
                    ) * int(new_product_quantity)
                    cart_obj.total_quantity += 1
                    cart_obj.save()

            return redirect("add_ord")

        elif "done" in request.POST:
            return redirect("edit_ord")

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


def generate_csv_response(data, header, filename):
    csv_content = ",".join(header) + "\n"
    for row in data:
        csv_content += ",".join(map(str, row)) + "\n"

    response = HttpResponse(csv_content, content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    return response


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

        if self.request.GET.get("format") == "csv":
            data = list(zip(product_names, quantities))
            header = ["Product Name", "Quantity Ordered"]
            return generate_csv_response(data, header, "popular_items")

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

        if self.request.GET.get("format") == "csv":
            data = list(zip(customer_numbers, total_sales))
            header = ["Customer Number", "Total Sales"]
            return generate_csv_response(data, header, "sales_by_customer")

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
        peak_hour = [hour["hour"] for hour in hours]
        order_counts = [hour["order_count"] for hour in hours]

        if self.request.GET.get("format") == "csv":
            data = list(zip(peak_hour, order_counts))
            header = ["Hour", "Order Count"]
            return generate_csv_response(data, header, "peak_business_hours")

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

        if self.request.GET.get("format") == "csv":
            data = list(zip(category_names, total_sales))
            header = ["Category Name", "Total Sales"]
            return generate_csv_response(data, header, "sales_by_category")

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

        if self.request.GET.get("format") == "csv":
            data = list(zip(phone_numbers, total_sales))
            header = ["Employee Phone Number", "Total Sales"]
            return generate_csv_response(data, header, "sales_by_employee")

        return JsonResponse(
            {"phone_numbers": phone_numbers, "total_sales": total_sales}
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

        if self.request.GET.get("format") == "csv":
            data = list(zip(product_names, quantities))
            header = ["Product Name", "Quantity Ordered (Morning)"]
            return generate_csv_response(data, header, "popular_items_morning")

        return JsonResponse({"product_names": product_names, "quantities": quantities})


class StatusCountView(View):
    def get(self, request):
        today = timezone.now().date()  # Just to ensure it's a date object without time
        accepted_carts_count = Cart.objects.filter(
            status=Cart.ACCEPT, time__date=today
        ).count()
        refused_carts_count = Cart.objects.filter(
            status=Cart.REFUSE, time__date=today
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

        if self.request.GET.get("format") == "csv":
            data = list(zip(product_names, quantities))
            header = ["Product Name", "Quantity Ordered"]
            return generate_csv_response(data, header, "top_selling_items")

        return JsonResponse({"product_names": product_names, "quantities": quantities})


def manager_dashboard(request):
    if request.user.is_authenticated:

        return render(request, "manager/manager_dashboard.html")
    else:
        messages.error(
                request, "You are NOT allowed to see staff panel", extra_tags="danger"
            )
        return redirect("staff_login")



class TotalSalesView(ListView):
    model = Cart

    def render_to_response(self, context, **response_kwargs):
        total_sales = Cart.objects.aggregate(total_sales=Sum("total_price"))[
            "total_sales"
        ]

        if self.request.GET.get("format") == "csv":
            csv_content = f"Total Sales\n{total_sales}"
            response = HttpResponse(csv_content, content_type="text/csv")
            response["Content-Disposition"] = 'attachment; filename="total_sales.csv"'
            return response

        return JsonResponse({"total_sales": total_sales})


class DailySalesView(ListView):
    model = Cart

    def render_to_response(self, context, **response_kwargs):
        daily_sales_data = (
            Cart.objects.annotate(day_of_week=ExtractWeekDay("time"))
            .values("day_of_week")
            .annotate(total_sales=Sum("total_price"))
            .order_by("day_of_week")
        )

        days = [item["day_of_week"] for item in daily_sales_data]
        sales = [item["total_sales"] for item in daily_sales_data]

        days_of_week = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        day_labels = [days_of_week[day - 1] for day in days]

        return JsonResponse({"days": day_labels, "daily_sales": sales})


class YearlySalesView(ListView):
    model = Cart

    def render_to_response(self, context, **response_kwargs):
        yearly_sales_data = (
            Cart.objects.annotate(year=ExtractYear("time"))
            .values("year")
            .annotate(total_sales=Sum("total_price"))
            .order_by("year")
        )

        years = [item["year"] for item in yearly_sales_data]
        sales = [item["total_sales"] for item in yearly_sales_data]

        return JsonResponse({"years": years, "yearly_sales": sales})


class MonthlySalesView(ListView):
    model = Cart

    def render_to_response(self, context, **response_kwargs):
        monthly_sales_data = (
            Cart.objects.annotate(month=ExtractMonth("time"))
            .values("month")
            .annotate(total_sales=Sum("total_price"))
            .order_by("month")
        )

        months = [item["month"] for item in monthly_sales_data]
        sales = [item["total_sales"] for item in monthly_sales_data]

        month_labels = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        month_names = [month_labels[month - 1] for month in months]

        return JsonResponse({"months": month_names, "monthly_sales": sales})
