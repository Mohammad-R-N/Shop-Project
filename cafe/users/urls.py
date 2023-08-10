from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserView.as_view(), name="users"),
    path("staff/", views.StaffPanelView.as_view(), name="staff"),
    path("stafflogin/", views.StaffLogin.as_view(), name="login"),
    path("stafflogin/staff/otp/", views.CheckOtp.as_view(), name="check-otp"),
    path("logout/", views.LogOutView.as_view(), name="logout_user"),
    path(
        "staff/order/<int:id>/",
        views.StaffOrderDetail.as_view(),
        name="staff_order_detail",
    ),
]
