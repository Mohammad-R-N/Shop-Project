from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import StaffLoginForm, StaffOtpForm
from django.views import View
from cart.models import OrderItem, Table
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
from .utils import StaffPanel, StaffEditOrd, StaffAddOrd, ExportCsv, Customer, Manager


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
    template_staff_accept_ord = "staff/staff_accepted.html"
    template_staff_refuse_ord = "staff/staff_refused.html"
    template_staff_search = "staff/staff_search_result.html"
    con = StaffPanel
    tables = Table.objects.all()
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = self.con.waiting_post(Cart)
            context = {"item": result[0], "cart": result[1], "table": self.tables}
            return render(request, self.template_staff, context)
        else:
            messages.error(
                request, "You are NOT allowed to see staff panel", extra_tags="danger"
            )
            return redirect("staff_login")

    def post(self, request):
        if "accepted_ord" in request.POST:
            result = self.con.accept_ord(request)
            context = {"item": result[0], "cart": result[1]}
            return render(request, self.template_staff_accept_ord, context)

        elif "refused_ord" in request.POST:
            result = self.con.refuse_ord(request)
            context = {"item": result[0], "cart": result[1]}
            return render(request, self.template_staff_refuse_ord, context)

        elif "waiting_ord" in request.POST:
            return redirect("staff")

        elif "phone_number" in request.POST:
            result = self.con.get_ord_by_phone(request)
            context = {"items": result[0], "carts": result[1], "table": self.tables, "query": result[2]}
            return render(request, self.template_staff_search, context)
        
        elif "date" in request.POST:
            result = self.con.get_ord_by_date(request)
            context = {"items": result[0], "carts": result[1], "table": self.tables, "query": result[2]}
            return render(request, self.template_staff_search, context)

        elif "table" in request.POST:
            result = self.con.get_ord_by_table(request)
            context = {"items": result[0], "carts": result[1], "table": self.tables, "query": result[2]}
            return render(request, self.template_staff_search, context)
        
        elif "refuse" in request.POST:
            self.con.make_refuse(request, Cart)
            return redirect("staff")

        elif "accept" in request.POST:
            self.con.make_accept(request, Cart)
            return redirect("staff")

        elif "edit" in request.POST:
            cart_edit_id = request.POST["edit"]
            request.session["edit_id"] = cart_edit_id
            return redirect("edit_ord")


class EditOrder(View):
    template_name = "staff/edit_ord.html"
    con = StaffEditOrd

    def get(self, request):
        if request.session.has_key("edit_id"):
            result = self.con.get_ord_for_edit(request, Cart)
            context = {
                "items": result[0],
                "cart": result[1],
            }
            return render(request, self.template_name, context)

        else:
            return render(request, self.template_name)

    def post(self, request):
        if "remove" in request.POST:
            result = self.con.remove_ord(request, Cart)
            if result:
                return redirect("edit_ord")
            else:
                return HttpResponse("hi")

        elif "done" in request.POST:
            result = self.con.save_new_quantity(request, OrderItem)
            if result:
                return redirect("staff")

        elif "add_ord" in request.POST:
            return redirect("add_ord")


class AddOrder(View):
    template_name = "staff/staff_add_order.html"
    con = StaffAddOrd

    def get(self, request):
        cat = Category.objects.all()
        product = Product.objects.all()
        context = {"category": cat, "product": product}
        return render(request, self.template_name, context)

    def post(self, request):
        if "add" in request.POST:
            result = self.con.add_ord_to_shop_cart(request, Product)
            if result:
                return redirect("add_ord")

        elif "done" in request.POST:
            return redirect("edit_ord")

        elif "all" in request.POST:
            cat = Category.objects.all()
            product = Product.objects.all()
            context = {"category": cat, "product": product}
            return render(request, self.template_name, context)
        else:
            result = self.con.show_product_in_cat(request, Product, Category)
            context = {"category": result[0], "product": result[1]}
            return render(request, self.template_name, context)


class PopularItemsView(ListView):
    model = OrderItem
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "popular_items")

        return JsonResponse({"product_names": product_names, "quantities": quantities})


class SalesByCustomerView(ListView):
    model = Cart
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "sales_by_customer")

        return JsonResponse(
            {"customer_numbers": customer_numbers, "total_sales": total_sales}
        )


class PeakBusinessHourView(ListView):
    model = Cart
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "peak_business_hours")

        return JsonResponse({"peak_hour": peak_hour})


class SalesByCategoryView(ListView):
    model = OrderItem
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "sales_by_category")

        return JsonResponse(
            {"category_names": category_names, "total_sales": total_sales}
        )


class SalesByEmployeeView(ListView):
    model = Cart
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "sales_by_employee")

        return JsonResponse(
            {"phone_numbers": phone_numbers, "total_sales": total_sales}
        )


class CustomerHistory(View):
    template_login = "manager/history_login_manager.html"
    template_history = "manager/history_for_manager.html"
    con = Customer

    def get(self, request):
        return render(request, self.template_login)

    def post(self, request):
        if "tel" in request.POST:
            result = self.con.get_ord_by_phone(request, Cart)
            context = {"items": result[0], "carts": result[1]}
            return render(request, self.template_history, context)
        else:
            return render(request, self.template_history)


class PopularItemsMorningView(ListView):
    model = OrderItem
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "popular_items_morning")

        return JsonResponse({"product_names": product_names, "quantities": quantities})


class StatusCountView(View):
    def get(self, request):
        today = timezone.now().date()
        result = Manager.status_count(request, today, Cart)
        return JsonResponse(result)


class OrderStatusReportView(View):
    def get(self, request):
        today = timezone.now().today().date()
        result = Manager.status_order(request, today, Cart)
        return JsonResponse(result)


class TopSellingItemsView(ListView):
    model = OrderItem
    csv = ExportCsv.generate_csv_response

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
            return self.csv(data, header, "top_selling_items")

        return JsonResponse({"product_names": product_names, "quantities": quantities})


class ManagerDashboard(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(
                request,
                "You need to be authenticated to access this page.",
                extra_tags="danger",
            )
            return redirect("staff_login")

        if not request.user.has_perm("users.can_access_dashboard"):
            messages.error(
                request,
                "You don't have permission to access this page.",
                extra_tags="danger",
            )
            return redirect("staff_login")

        return render(request, "manager/manager_dashboard.html")


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
