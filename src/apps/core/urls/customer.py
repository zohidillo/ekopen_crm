from django.urls import path

import src.apps.core.views.customers as view

urlpatterns = [
    path("list", view.CustomerListView.as_view(), name="customer-list"),
    path("create", view.CustomerCreateView.as_view(), name="customer-create"),
    path("<int:pk>", view.CustomerDetailView.as_view(), name="customer-detail"),
    path("update/<int:pk>", view.CustomerUpdateView.as_view(), name="customer-update"),
]
