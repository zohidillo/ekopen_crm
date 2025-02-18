from django.urls import path, include

urlpatterns = [
    path("products/", include("src.apps.core.api.urls.product")),
    path("customer/", include("src.apps.core.api.urls.customer")),
]
