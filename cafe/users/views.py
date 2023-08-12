from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import StaffLoginForm,StaffOtpForm
from django.views import View
from cart.models import OrderItem
import random
from utils import send_OTP
from .models import CustomUser

class UserView(View):
    def get(self, request):
        return render(request,"users/staff.html")

    def post(self, request):
        pass

class StaffLogin(View):
    form_staff=StaffLoginForm
    def get(self, request):
        form = self.form_staff
        return render(request, "staff/login.html", {"form": form})

    def post(self, request):
        form = self.form_staff(request.POST)
        if form.is_valid():
            random_code=random.randint(1000,9999)
            print(random_code)
            CustomUser.objects.update(code=random_code)
            phone_number = form.cleaned_data.get("phone_number")
            send_OTP(phone_number,random_code)
            request.session["user_info"]={'phone_number':phone_number,"code":random_code}
            return redirect("check-otp")

class CheckOtp(View):
    form_otp=StaffOtpForm
    def get(self, request):
        form = self.form_otp()
        return render(request, "staff/otp.html", {"form": form})        
    def post(self, request):
        form = self.form_otp(request.POST)
        otp = form.cleaned_data.get("code")
        if form.is_valid():
            user = authenticate(request, phone_number=request.session["user_info"]["phone_number"], code=otp)
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
        orders = OrderItem.objects.all()
        context = {"orders": orders}
        return render(request, self.template_name, context)


