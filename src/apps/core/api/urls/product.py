from rest_framework.routers import DefaultRouter
from django.urls import path

import src.apps.core.api.view.product as view

router = DefaultRouter()
router.register("category/list", view.CategoryListAPIView)

urlpatterns = [
    path("list/", view.ProductListAPIView.as_view()),
    path("warehouse/list/", view.WarehouseProductListAPIView.as_view()),
]
urlpatterns += router.urls
