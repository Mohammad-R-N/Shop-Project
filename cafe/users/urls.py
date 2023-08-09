from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserView.as_view(), name="users"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogOutView.as_view(), name="logout_user"),
    path("staff/", views.StaffPanelView.as_view(), name="staff"),
    path('stafflogin/',views.StaffLogin.as_view(),name='staff-login')
]