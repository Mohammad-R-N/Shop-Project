from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserView.as_view(), name="users"),
    path("staff/", views.StaffPanelView.as_view(), name="staff"),
    path("edit_orders/", views.EditOrder.as_view(), name="edit_ord"),
    path("add_orders/", views.AddOrder.as_view(), name="add_ord"),
    path("stafflogin/", views.StaffLogin.as_view(), name="login"),
    path("stafflogin/staff/otp/", views.CheckOtp.as_view(), name="check-otp"),
    path("logout/", views.LogOutView.as_view(), name="logout_user"),
    path("dashboard/", views.ManagerDashboard.as_view(), name="dashboard")
]
