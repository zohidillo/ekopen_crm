from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from django.db import transaction

import src.documents.models as models
import src.apps.documents.api.serializers as serializers


class CreateDocOrderAPIView(CreateAPIView, GenericViewSet):
    """ creating doc order and doc order items together """
    queryset = models.DocOrder.objects.select_related("customer", "created_by", "modified_by")
    serializer_class = serializers.PostDocOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        items = data.pop("items", [])
        try:
            with transaction.atomic():
                doc = models.DocOrder.objects.create(created_by=user, customer_id=data.pop("customer"), **data)
                items_list = [
                    models.DocOrderItem(
                        doc_order=doc, created_by=user,
                        product_id=i.pop("product"), **i
                    )
                    for i in items
                ]
                models.DocOrderItem.objects.bulk_create(items_list)
                doc.calculate_total_sum()
                doc.save()
                return Response({"msg": "Doc order created", "order_id": doc.id}, status=HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
