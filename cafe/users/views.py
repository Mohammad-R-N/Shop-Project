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
import datetime
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

    def post(self, request):
        pass


class StaffPanelView(View):
    template_name = "staff/staff.html"

    def get(self, request, *args, **kwargs):
        customer_ord_info = request.session["reserve"]
        info_list = list()
        # del request.session["staff"]
        if request.session.has_key("staff"):
            data = request.session["staff"]
            context = {"order": data}
            return render(request, self.template_name, context)
        else:
            for ord_information in customer_ord_info:
                order_list = dict()
                order_detail = list()
                order = ord_information["orders"]
                for ord in order:
                    ords = ord.split('=')
                    order_detail.append(ords)

                order_list['ord_detail'] = order_detail
                order_list['number'] = ord_information['phone_number']
                order_list['quantity'] = len(order)
                order_list['total'] = ord_information['cost']
                order_list['table'] = ord_information['table']
                order_list['refuse'] = False
                order_list['accept'] = False
                info_list.append(order_list)

            request.session["staff"] = info_list
            context = {"order": info_list}
            return render(request, self.template_name, context)

    def post(self, request):
        if "refuse" in request.POST:
            refuse_ord = request.POST['refuse']
            info = request.session["staff"]
            edit_ord = list()
            for ord in info:
                if ord['number'] == refuse_ord:
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = True
                    data['accept'] = False
                    edit_ord.append(data)
                elif ord['refuse'] == True:
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = True
                    data['accept'] = False
                    edit_ord.append(data)
                else:
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = False
                    data['accept'] = False
                    edit_ord.append(data)

            request.session["staff"] = edit_ord
            return redirect('staff')
        
        elif "accept" in request.POST:
            accept_ord_number = request.POST['accept']
            info = request.session["staff"]
            edit_ord = list()
            for ord in info:
                if ord['number'] == accept_ord_number:
                    total = ord['total']
                    quantity = ord['quantity']
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = False
                    data['accept'] = True
                    edit_ord.append(data)
                elif ord['refuse'] == True:
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = True
                    data['accept'] = False
                    edit_ord.append(data)
                elif ord['accept'] == True:
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = False
                    data['accept'] = True
                    edit_ord.append(data)
                else:
                    data = dict()
                    data['number'] = ord['number']
                    data['quantity'] = ord['quantity']
                    data['total'] = ord['total']
                    data['ord_detail'] = ord['ord_detail']
                    data['table'] = ord['table']
                    data['refuse'] = False
                    data['accept'] = False
                    edit_ord.append(data)

            Cart.objects.create(total_price=total, total_quantity=quantity)
            request.session["staff"] = edit_ord
            return redirect('staff')

        elif "edit" in request.POST:
            edit_ord = request.POST['edit']
            info = request.session["staff"]
            ord_for_edit = dict()
            for ord in info:
                if ord['number'] == edit_ord:
                    ord_for_edit['number'] = ord['number']
                    ord_for_edit['quantity'] = ord['quantity']
                    ord_for_edit['total'] = ord['total']
                    ord_for_edit['ord_detail'] = ord['ord_detail']
                    ord_for_edit['table'] = ord['table']
            
            request.session["ord_for_edit"] = ord_for_edit
            return redirect('edit_ord')

class EditOrder(View):
    template_name = "staff/edit_ord.html"
    def get(self, request):
        ord_for_edit = request.session["ord_for_edit"]
        number = ord_for_edit['number']
        product = list()

        for edit_pt in ord_for_edit['ord_detail']:
            pt = Product.objects.get(name=edit_pt[0])
            data = dict()
            data['product_name'] = pt.name
            data['product_photo'] = pt.photo.url
            data['product_quantity'] = edit_pt[1]
            product.append(data)

        context = {
            "product": product,
            "number": number
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if "remove" in request.POST:
            remove_product = request.POST["remove"]
            remove_name = remove_product.split('-')[0]
            number = remove_product.split('-')[1]
            ord_for_edit = request.session["ord_for_edit"]
            data = request.session["staff"]
            ord_detail = list()
            edited_list = list()
            new_total = 0

            for edit_pt in ord_for_edit['ord_detail']:
                if edit_pt[0] != remove_name:
                    pt = Product.objects.get(name=edit_pt[0])
                    new_quantity = request.POST[f"{edit_pt[0]}"]
                    if new_quantity == '':
                        new_total += int(pt.price) * int(edit_pt[1])
                        ord_detail.append([edit_pt[0], edit_pt[1]])
                    else:
                        new_total += int(pt.price) * int(new_quantity)
                        ord_detail.append([edit_pt[0], new_quantity])

            for ord in data:
                if ord['number'] == number:
                    result = dict()
                    result['number'] = ord['number']
                    result['quantity'] = len(ord_detail)
                    result['total'] = new_total
                    result['ord_detail'] = ord_detail
                    result['table'] = ord['table']
                    result['refuse'] = False
                    request.session["ord_for_edit"] = result
                    edited_list.append(result)
                else:
                    if ord['refuse'] == True:
                        result = dict()
                        result['number'] = ord['number']
                        result['quantity'] = ord['quantity']
                        result['total'] = ord['total']
                        result['ord_detail'] = ord['ord_detail']
                        result['table'] = ord['table']
                        result['refuse'] = True
                        edited_list.append(result)
                    else:
                        result = dict()
                        result['number'] = ord['number']
                        result['quantity'] = ord['quantity']
                        result['total'] = ord['total']
                        result['ord_detail'] = ord['ord_detail']
                        result['table'] = ord['table']
                        result['refuse'] = False
                        edited_list.append(result)

            request.session["staff"] = edited_list
            return redirect("edit_ord")

        elif "done" in request.POST:
            number = request.POST["done"]
            ord_for_edit = request.session["ord_for_edit"]
            data = request.session["staff"]
            ord_detail = list()
            edited_list = list()
            new_total = 0
            for edit_pt in ord_for_edit['ord_detail']:
                if edit_pt[0] in request.POST:
                    pt = Product.objects.get(name=edit_pt[0])
                    new_quantity = request.POST[f"{edit_pt[0]}"]
                    if new_quantity == '':
                        new_total += int(pt.price) * int(edit_pt[1])
                        ord_detail.append([edit_pt[0], edit_pt[1]])
                    else:
                        new_total += int(pt.price) * int(new_quantity)
                        ord_detail.append([edit_pt[0], new_quantity])
            
            for ord in data:
                if ord['number'] == number:
                    result = dict()
                    result['number'] = ord['number']
                    result['quantity'] = len(ord_detail)
                    result['total'] = new_total
                    result['ord_detail'] = ord_detail
                    result['table'] = ord['table']
                    result['refuse'] = False
                    edited_list.append(result)
                else:
                    if ord['refuse'] == True:
                        result = dict()
                        result['number'] = ord['number']
                        result['quantity'] = ord['quantity']
                        result['total'] = ord['total']
                        result['ord_detail'] = ord['ord_detail']
                        result['table'] = ord['table']
                        result['refuse'] = True
                        edited_list.append(result)
                    else:
                        result = dict()
                        result['number'] = ord['number']
                        result['quantity'] = ord['quantity']
                        result['total'] = ord['total']
                        result['ord_detail'] = ord['ord_detail']
                        result['table'] = ord['table']
                        result['refuse'] = False
                        edited_list.append(result)

            request.session["staff"] = edited_list
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
            pt_name = request.POST["add"]

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
    today = datetime.datetime.today()

    def get(self, request):
        daily_order = Cart.objects.filter(time=self.today)
        orders = Cart.objects.all()

        today_discount = 0
        for ord in daily_order:
            today_discount += ord.discount
        avg_today_discount = today_discount / len(daily_order)

        today_order = 0 
        for ord in daily_order:
            today_order += 1

        today_sales = 0
        for ord in today_order:
            today_sales += ord.total_price

        total_sales = 0
        for ord in orders:
            total_sales += 1

        total_order = 0
        for ord in orders:
            total_order += 1

        data = {
            'avg_today_discount': avg_today_discount,
            'today_order': today_order,
            'today_sales': today_sales,
            'total_sales': total_sales,
            'total_order': total_order,
        }

        context = {
            "data": data,
        }

        return render(request, self.template_name, context)
        # return render(request, self.template_name)
