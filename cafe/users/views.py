from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm,StaffLoginForm
from django.views import View
from cart.models import OrderItem
from menu.models import Product


# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_user")

class UserView(View):
    def get(self, request):
        return render(request,"users/staff.html")

    def post(self, request):
        pass

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")

    def post(self, request):
        pass

def logout_user(request):
    logout(request)
    return redirect("home")


class StaffPanelView(View):
    template_name = "staff/staff.html"
    
    def get(self, request, *args, **kwargs):
        customer_info = request.session['reserve']
        order = customer_info['orders']
        product_list = list()
        for name in order:
            product = Product.objects.get(name=name)
            product_list.append(product)
        context = {
                    "order": product_list,
                    "info": customer_info
                }
        return render(request, self.template_name, context)

class StaffOrderDetail(View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Product, id=kwargs['id'])
        customer_info = request.session['reserve']
        order = customer_info['orders']

class StaffLogin(View):
    form_staff=StaffLoginForm
    def get(self,request):
        form=self.form_staff
        return render(request,"staff/login.html",{"form":form})

    def post(self,request):
        pass

