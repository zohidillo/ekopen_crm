from django.urls import path
from rest_framework.routers import DefaultRouter

import src.apps.documents.api.views.sales as view

router = DefaultRouter()
router.register("list", view.DocOrderView)
router.register("create", view.CreateDocOrderAPIView, basename="doc_order_create")
router.register("detail", view.DetailDocOrderAPIView, basename="doc_order_detail")

urlpatterns = [
                  path("get-waybill/<int:id>", view.GetWaybillDocument.as_view(), name="get_waybill"),
              ] + router.urls
