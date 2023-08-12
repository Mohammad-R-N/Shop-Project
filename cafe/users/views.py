from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import StaffLoginForm, StaffOtpForm
from django.views import View
from cart.models import OrderItem
import random
from utils import send_OTP
from .models import CustomUser
from menu.models import Product
from .authentication import CustomAuthBackend
import re


class UserView(View):
    def get(self, request):
        return render(request, "users/staff.html")

    def post(self, request):
        pass


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
        otp = form.cleaned_data.get("code")
        if form.is_valid():
            user = authenticate(
                request,
                phone_number=request.session["user_info"]["phone_number"],
                code=otp,
            )
            if user is not None:
                login(request, user)
                return redirect("staff/")
            return redirect("/")


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")

    def post(self, request):
        pass


class StaffPanelView(View):
    template_name = "staff/staff.html"

    def get(self, request, *args, **kwargs):
        customer_info = request.session["reserve"]
        order = customer_info["orders"]
        product_list = list()
        for name in order:
            product = Product.objects.get(name=name)
            product_list.append(product)
        context = {"order": product_list, "info": customer_info}
        return render(request, self.template_name, context)


class StaffOrderDetail(View):
    template_name = "staff/staff_order_detail.html"

    def get(self, request, *args, **kwargs):
        order_id = kwargs["id"]
        order = get_object_or_404(OrderItem, id=order_id)
        order_items = OrderItem.objects.filter(
            order=order
        )  # Getting all OrderItem objects related to this order

        context = {"order": order, "order_items": order_items}
        return render(request, self.template_name, context)

