from django.urls import path
from . import views

urlpatterns = [
    path("staff/", views.StaffPanelView.as_view(), name="staff"),
    path('stafflogin/',views.StaffLogin.as_view(),name='login'),
    path('stafflogin/staff/otp/',views.CheckOtp.as_view(),name="check-otp")
]