from django.urls import path, include

urlpatterns = [
    path("", include("src.apps.core.urls.auth")),
    path("product/", include("src.apps.core.urls.products")),
    path("payments/", include("src.apps.core.urls.payments")),
    path("customers/", include("src.apps.core.urls.customer")),

    path("document/warehouse/", include("src.apps.documents.urls.warehouse")),
    path("document/purchase/", include("src.apps.documents.urls.doc_purchase")),
    path("document/purchase-return/", include("src.apps.documents.urls.doc_purchase_return")),

    path("document/sales/", include("src.apps.documents.urls.order")),
    path("document/sales-return/", include("src.apps.documents.urls.order_return")),

    path("reports/", include("src.apps.documents.urls.reports")),
]

url_apis = [
    path("api/", include("src.apps.core.api.urls.base")),
    path("api/", include("src.apps.documents.api.urls.base")),
]

urlpatterns += url_apis
