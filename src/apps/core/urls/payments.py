from django.urls import path

import src.apps.core.views.payments as view

urlpatterns = [
    path("customer/create", view.create_payment_history, name="customer-payment-create"),
    path("customer/list", view.CustomerPaymentsListView.as_view(), name="customer-payment-list"),
    path("customer/update/<int:pk>", view.update_payment_history, name="customer-payment-update"),

    path("organization/list", view.OrganizationPaymentsListView.as_view(), name="organization-payment-list"),
    path("organization/create", view.create_organization_payment_history, name="organization-payment-create"),
    path("organization/update/<int:pk>", view.update_organization_payment_history,
         name="organization-payment-update"),

]
