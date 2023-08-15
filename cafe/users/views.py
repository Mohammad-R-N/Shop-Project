from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import StaffLoginForm, StaffOtpForm
from django.views import View
from cart.models import OrderItem
import random
from utils import send_OTP
from .models import CustomUser
from menu.models import Product, Category
from cart.models import Cart
from .authentication import CustomAuthBackend
import re
from django.utils import timezone
from django.db.models import Sum

class UserView(View):
    def get(self, request):
        return render(request, "users/staff.html")


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
            formatted_phone_number = re.sub(r'^\+98|^0098', '0', phone_number)

            user = CustomUser.objects.filter(phone_number=formatted_phone_number).first()
            if user is None:
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
                return redirect("staff")
            return redirect("home")
        return redirect('menu')

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")

class StaffPanelView(View):
    template_staff = "staff/staff.html"
    # template_staff_login = "staff/login.html"

    def get(self, request, *args, **kwargs):
        # return redirect("staff_login")
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

    def post(self, request):
        if "refuse" in request.POST:
            cart_refuse_id = request.POST['refuse']
            cart = Cart.objects.all()

            for cart_obj in cart:
                if cart_obj.id == int(cart_refuse_id):
                    update_cart = Cart.objects.get(id=cart_obj.id)
                    update_cart.status = "r"
                    update_cart.save()

            return redirect("staff")
        
        elif "accept" in request.POST:
            cart_accept_id = request.POST['accept']
            cart = Cart.objects.all()

            for cart_obj in cart:
                if cart_obj.id == int(cart_accept_id):
                    update_cart = Cart.objects.get(id=cart_obj.id)
                    update_cart.status = "a"
                    update_cart.save()

            return redirect("staff")
        
        elif "edit" in request.POST:
            cart_edit_id = request.POST['edit']
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
            return redirect('add_ord')

class AddOrder(View):
    template_name = "staff/staff_add_order.html"
    
    def get(self, request):
        cat = Category.objects.all()
        product = Product.objects.all()
        context = {
            "category": cat,
            "product": product
        }
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
                    order_item = OrderItem.objects.create(product=new_product_obj, cart=cart_obj, 
                                                            quantity=int(new_product_quantity), price=new_product_obj.price)
                    order_item.save()

        elif 'all' in request.POST:
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
        
        #Most_Popular_Product

        #Peak_Business_hour

        #Customer_Order_History
        
        data = {
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
