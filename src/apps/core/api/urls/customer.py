from rest_framework.routers import DefaultRouter
from django.urls import path

import src.apps.core.api.view.customer as view

router = DefaultRouter()
router.register("list", view.CustomerListAPIView)

urlpatterns = [
    path("pay", view.CustomerDebtPaymentView.as_view())
]
urlpatterns += router.urls
