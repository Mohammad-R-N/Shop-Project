from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import StaffLoginForm, StaffOtpForm
from django.views import View
from cart.models import OrderItem
import random
from django.db.models.functions import ExtractHour
from utils import send_OTP
from .models import CustomUser
from menu.models import Product, Category
from cart.models import Cart
from .authentication import CustomAuthBackend
import re
from django.db.models import Sum, Count
from django.utils import timezone
from django.db.models import Sum
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
                messages.error(request, 'User not found!', 'danger')
                return redirect("login")  # Redirect to signup page if user is not registered
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
            user = CustomAuthBackend.authenticate(request, phone_number=request.session["user_info"]["phone_number"], code=otp)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Loged In Successfully', 'success')
                return redirect("staff")
            messages.error(request, 'OTP code is NOT CORRECT!', 'danger')
            return redirect("home")
        return redirect('menu')


class LogOutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'LogOut Successfully!', 'success')
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
                    item.append(items)
                    carts.append(cart_obj)

            context = {
                'item': item,
                'cart': carts
            }
            return render(request, self.template_staff, context)
        else:
            messages.error(request,"You are NOT allowed to see staff panel",extra_tags="danger")
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

            context = {
                'item': item,
                'cart': carts
            }
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

            context = {
                'item': item,
                'cart': carts
            }
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

            context = {
                "items": item_list,
                "carts": cart_list
                }
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
                    messages.success(request, 'Refused successfully!', 'warning')
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
                    messages.success(request, 'Accepted successfully!', 'success')
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
                    items = OrderItem.objects.get(cart=cart_obj)
                    item_list.append(items)

            for item in item_list:
                if item.id == int(order_item_id):
                    OrderItem.objects.get(id=int(order_item_id)).delete()
                    messages.success(request, 'Deleted successfully!', 'warning')
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
            
            return redirect('add_ord')
        
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


class ManagerDashboard(View):

    template_name = 'manager/manager_dashboard.html'
    today = timezone.now().today().date()
    week = today - timezone.timedelta(days=7)
    month = today - timezone.timedelta(days=30)
    year = today - timezone.timedelta(days=365)

    def get(self, request):
        all_cart = Cart.objects.all()
        all_accepted_cart = Cart.objects.filter(status="a")
        daily_order = Cart.objects.filter(status="a").filter(time=self.today)
        weekly_order = Cart.objects.filter(status="a").filter(time=self.week)
        monthly_order = Cart.objects.filter(status="a").filter(time=self.month)
        yearly_order = Cart.objects.filter(status="a").filter(time=self.year)

        #Daily
        daily_sales = daily_order.aggregate(daily_sales=Sum("total_price"))["daily_sales"]
        daily_order_count = daily_order.count()

        #Weekly
        weekly_sales = daily_order.aggregate(weekly_sales=Sum("total_price"))["weekly_sales"]
        weekly_order_count = weekly_order.count()

        #Monthly
        monthly_sales = daily_order.aggregate(monthly_sales=Sum("total_price"))["monthly_sales"]
        monthly_order_count = monthly_order.count()

        #Yearly
        yearly_sales = daily_order.aggregate(yearly_sales=Sum("total_price"))["yearly_sales"]
        yearly_order_count = yearly_order.count()

        #Total
        total_sales = all_accepted_cart.aggregate(daily_sales=Sum("total_price"))["total_sales"]
        total_order_count = all_accepted_cart.count()
        
    
        
        data = {

            # "avg_today_discount": avg_today_discount,
            # "today_order": today_order,
            # "today_sales": today_sales,
            # "total_sales": total_sales,
            # "total_order": total_order,
            "daily_sales": daily_sales,
            "daily_order_count": daily_order_count,
            "weekly_sales": weekly_sales,
            "weekly_order_count": weekly_order_count,
            "monthly_sales": monthly_sales,
            "monthly_order_count": monthly_order_count,
            "yearly_sales": yearly_sales,
            "yearly_order_count": yearly_order_count,
            "total_sales": total_sales,
            "total_order_count": total_order_count,

        }

        context = {
            "data": data,
        }

        return render(request, self.template_name, context)

        # return render(request, self.template_name)


def popular_items(request):
    items = (
        (OrderItem.objects.values("product__name"))
        .annotate(total_ordered=Sum("quantity"))
        .order_by("-total_ordered")[:5]
    )

    return render(request, "dashboard1.html", {"items": items})


def sales_by_customer(request):
    sales = (
        Cart.objects.values("customer_number")
        .annotate(total_sales=Sum("total_price"))
        .order_by("-total_sales")[:3]
    )
    return render(request, "sales_by_customer.html"), {"sales": sales}


def peak_business_hour(request):
    hours = (
        Cart.objects.annotate(hour=ExtractHour("time"))
        .values("hour")
        .annotate(order_count=Count("id"))
        .order_by("-order_count")[:1]
    )
    peak_hour = hours[0] if hours else None

    return render(request, "peak_hour", {"peak_hour": peak_hour})


def sales_by_category(request):
    categories = (
        OrderItem.objects.select_related("product")
        .values("product__category_menu__name")
        .annotate(total_sales=Sum("price"))
        .order_by("-total_sales")
    )
    return render(request, "sales_by_category.html", {"categories": categories})


def sales_by_employee(request):
    sales = (
        Cart.objects.values("cart_users__phone_number")
        .annotate(total_sales=Sum("total_price"))
        .order_by("-total_sales")[:3]
    )
    return render(request, "sales_by_employee.html"), {"sales": sales}

def customer_order_history(request):
    customers = CustomUser.objects.all()
    orders = []
    for customer in customers:
        customer_orders = (
            Cart.objects.filter(customer_number=customer.phone_number)
            .prefetch_related("items__product")
            .annotate(total_spent=Sum("items__price"))
            .order_by("-time")
        )
        orders.append({"customer": customer, "orders": customer_orders})
    context = {"orders": orders}
    return render(request, "customer_order_history.html", context)

def popular_items_morning(request):

    start_time = timezone.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = timezone.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    items = (
        OrderItem.objects.filter(cart__time__range=(start_time, end_time))
        .values("product__name")
        .annotate(total_ordered=Sum("quantity"))
        .order_by("-total_ordered")[:2]
    )

    return render(request, "popular_items_morning.html", {"items": items})


def status_count(request):
    today = timezone.now().today().date()

    accepted_carts_count = Cart.objects.filter(status="a", time = today).count()
    refused_carts_count = Cart.objects.filter(status="r", time = today).count()
    total_carts_count = accepted_carts_count + refused_carts_count

    accepted_percentage = (accepted_carts_count / total_carts_count) * 100
    refused_percentage = (refused_carts_count / total_carts_count) * 100

    context = {
        "accepted_count": accepted_carts_count,
        "refused_count": refused_carts_count,
        "accepted_percentage": accepted_percentage,
        "refused_percentage": refused_percentage,
    }

    return render(request, "status_count.html", context)
