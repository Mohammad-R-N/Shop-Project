from django.urls import path
from . import views
from .views import StaffPanelView

urlpatterns = [
    path("", views.users_page, name="users"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout_user"),
    path("staff/", StaffPanelView.as_view(), name="staff"),
]
