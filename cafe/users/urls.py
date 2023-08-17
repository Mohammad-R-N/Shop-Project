from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path("", views.UserView.as_view(), name="users"),
    path("staff/", views.StaffPanelView.as_view(), name="staff"),
    path("edit_orders/", views.EditOrder.as_view(), name="edit_ord"),
    path("add_orders/", views.AddOrder.as_view(), name="add_ord"),
    path("stafflogin/", views.StaffLogin.as_view(), name="staff_login"),
    # path("stafflogin/staff/otp/", views.CheckOtp.as_view(), name="check-otp"),
    path("logout/", views.LogOutView.as_view(), name="logout_user"),
    path("dashboard/", views.manager_dashboard, name="dashboard"),
    path("popular_items/", PopularItemsView.as_view(), name="popular_items"),
    path("sales_by_customer/", SalesByCustomerView.as_view(), name="sales_by_customer"),
    path(
        "peak_business_hour/", PeakBusinessHourView.as_view(), name="peak_business_hour"
    ),
    path("sales_by_category/", SalesByCategoryView.as_view(), name="sales_by_category"),
    path("sales_by_employee/", SalesByEmployeeView.as_view(), name="sales_by_employee"),
    path(
        "history_for_manager/",
        views.CustomerHistory.as_view(),
        name="history_for_manager",
    ),
    path(
        "popular_items_morning/",
        PopularItemsMorningView.as_view(),
        name="popular_items_morning",
    ),
    path("status_count/", StatusCountView.as_view(), name="status_count"),
    path(
        "order_status_report/",
        OrderStatusReportView.as_view(),
        name="order_status_report",
    ),
    path("top_selling_items/", TopSellingItemsView.as_view(), name="top_selling_items"),
    path("total_sales/", TotalSalesView.as_view(), name="total_sales"),
    path("daily_sales/", DailySalesView.as_view(), name="daily_sales"),
    path("monthly_sales/", MonthlySalesView.as_view(), name="monthly_sales"),
    path("yearly_sales/", YearlySalesView.as_view(), name="yearly_sales"),
]
