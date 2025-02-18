from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from django.shortcuts import get_object_or_404

import src.documents.models as models
from src.apps.utils.generate_pdf import generate_pdf
import src.apps.documents.api.serializers as serializers
from django.db.models import F, ExpressionWrapper, DecimalField


class DocOrderView(ListAPIView, GenericViewSet):
    queryset = models.DocOrder.objects.select_related("customer")
    serializer_class = serializers.SaleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        customer = self.request.query_params.get("customer")
        if customer:
            # Annotate the queryset with the remaining balance calculation
            qs = qs.filter(customer=customer).annotate(
                remaining_balances=ExpressionWrapper(
                    F('total_sum') - F('paid_amount'),
                    output_field=DecimalField()
                )
            ).filter(remaining_balances__gt=0)
        return qs


class GetWaybillDocument(APIView):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order = get_object_or_404(models.DocOrder, id=order_id)
        path = generate_pdf(order, request)
        order.waybill_path = path
        order.save()
        waybill_path = order.waybill_path

        if not waybill_path:
            return Response({"error": "Waybill path mavjud emas"}, status=HTTP_404_NOT_FOUND)

        return Response({"waybill_path": waybill_path}, status=HTTP_200_OK)
