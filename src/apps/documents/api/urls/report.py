from django.urls import path

import src.apps.documents.api.views.report as view

sale = [
    path("sales/category/", view.SaleReportCategoryAPIView.as_view(), name="sale_category"),
    path("sales/month/", view.MonthSalesReportAPIView.as_view(), name="sale_month"),
]

customer = [
    path("customer/top/", view.TopCustomerReportView.as_view(), name="report-top-customer"),
]

urlpatterns = [] + sale + customer
