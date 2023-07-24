from django.shortcuts import render

# Create your views here.
def customer_page(request):
    return render(request,"customer/customer.html")