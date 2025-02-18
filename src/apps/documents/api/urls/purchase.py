from rest_framework.routers import DefaultRouter

import src.apps.documents.api.views.purchase as view

router = DefaultRouter()
router.register("list", view.DocPurchaseListView)
router.register("detail", view.DocPurchaseItemDetailView)

urlpatterns = [] + router.urls
