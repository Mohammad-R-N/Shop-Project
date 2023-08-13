from django.shortcuts import render, redirect, HttpResponse
from django.views import View


# Create your views here.
class CustomerView(View):
    def get(self, request):
        return render(request,"customer/customer.html")
    def post(self, request):
        pass

class CustomerHistory(View):
    template_name = "customer/history_login.html"
    def get(self, request):
        ord_history = request.session['reserve']
        print(ord_history)
        return render(request, self.template_name)
    
    def post(self, request):
        if 'tel' in request.POST:
            number = request.POST['tel']
            ord_history = request.session['reserve']
            print(ord_history)
            result = list()

            for ord in ord_history:
                if ord['phone_number'] == number:
                    data = dict()
                    data['number'] = ord['phone_number']
                    data['table'] = ord['table']
                    data['total'] = ord['cost']
                    data['date'] = ord['date']
                    order_detail = list()
                    order = ord["orders"]
                    for ord in order:
                        ords = ord.split('=')
                        order_detail.append(ords)
                    data['orders'] = order_detail
                    data['quantity'] = len(order_detail)
                    result.append(data)
            
            context = {"order": result}
            return render(request, "customer/history.html", context)         