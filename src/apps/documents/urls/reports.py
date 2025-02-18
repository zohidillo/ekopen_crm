from django.urls import path

import src.apps.documents.views.reports as views

urlpatterns = [
    path("sales/", views.report_sale, name="report-sales"),
    path("customer/", views.report_customer, name="report-customer"),
]
