from django.urls import path
from . import views

urlpatterns = [
    path("", views.users_page, name="users"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout_user"),
    path("staff/", views.StaffPanelView.as_view(), name="staff"),
    path('stafflogin/',views.StaffLogin.as_view(),name='staff-login')
]
