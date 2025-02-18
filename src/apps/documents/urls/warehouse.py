from django.urls import path

import src.apps.documents.views.warehouse as view

urlpatterns = [
    path("list", view.WarehouseListView.as_view(), name="warehouse-list"),
    path("update/<int:pk>", view.update_quantity, name="warehouse-update"),
]
