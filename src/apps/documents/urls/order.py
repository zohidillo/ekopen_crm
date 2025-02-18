from django.urls import path

import src.apps.documents.views.sale as views

urlpatterns = [
    path("create", views.create_order, name="order-create"),
    path("update/<int:pk>", views.update_order, name="order-update"),
    path("test/waybill/<int:pk>", views.waybill, name="waybill-test"),
    path("list", views.SaleOrderListView.as_view(), name="order-list"),
]
