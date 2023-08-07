from django.shortcuts import render

# Create your views here.
def users_page(request):
    return render(request,"users/staff.html")