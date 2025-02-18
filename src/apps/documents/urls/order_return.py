from django.urls import path

import src.apps.documents.views.sale as views

urlpatterns = [
    path("create", views.create_order_return, name="order-return-create"),
    path("list", views.ReturnOrderListView.as_view(), name="order-return-list"),
    path("update/<int:pk>", views.update_order_return, name="order-return-update"),
]
