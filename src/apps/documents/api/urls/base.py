from django.urls import path, include


urlpatterns = [
    path("sales/", include("src.apps.documents.api.urls.sale")),
    path("report/", include("src.apps.documents.api.urls.report")),
    path("purchase/", include("src.apps.documents.api.urls.purchase")),
    path("analytics/", include("src.apps.documents.api.urls.analytics")),
]
