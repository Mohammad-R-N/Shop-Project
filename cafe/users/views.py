from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm,StaffLoginForm
from django.views import View
from django.views.generic import TemplateView
from cart.models import OrderItem


# Create your views here.
def users_page(request):
    return render(request, "users/staff.html")


def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "staff/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = CustomAuthenticationForm()
    return render(request, "staff/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")


class StaffPanelView(TemplateView):
    template_name = "staff/staff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = OrderItem.objects.all()
        return context

class StaffLogin(View):
    form_staff=StaffLoginForm
    def get(self,request):
        form=self.form_staff
        return render(request,"staff/login.html",{"form":form})

    def post(self,request):
        pass