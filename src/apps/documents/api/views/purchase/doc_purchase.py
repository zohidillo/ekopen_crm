from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView

import src.documents.models as models
import src.apps.documents.api.serializers as serializers
from django.db.models import F, ExpressionWrapper, DecimalField


class DocPurchaseItemDetailView(RetrieveAPIView, GenericViewSet):
    queryset = models.DocPurchaseItem.objects.select_related("product")
    serializer_class = serializers.DocPurchaseItemSerializer


class DocPurchaseListView(ListAPIView, GenericViewSet):
    queryset = models.DocPurchase.objects.order_by("-id")
    serializer_class = serializers.DocPurchaseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            remaining_balances=ExpressionWrapper(
                F('total_purchase_sum') - F('paid_amount'),
                output_field=DecimalField()
            )
        ).filter(remaining_balances__gt=0)
        return qs
