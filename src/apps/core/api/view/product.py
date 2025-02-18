from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet

from django.db.models import OuterRef, Subquery

import src.core.models as models
import src.documents.models as document_models
import src.apps.core.api.serializers as serializers


class CategoryListAPIView(ListAPIView, GenericViewSet):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductListAPIView(APIView):
    def get(self, request):
        qs = models.Product.objects.select_related('category', "created_by", "modified_by")
        party = self.request.query_params.get('party', None)
        category = self.request.query_params.get('category', None)

        if party:
            party_items = document_models.DocPurchaseItem.objects.filter(doc_purchase_id=party)
            items = [item.product.pk for item in party_items]
            qs = qs.filter(id__in=items)

        if category:
            qs = qs.filter(category__id=category)

        qs = qs.annotate(
            party_item_quantity=Subquery(
                document_models.DocPurchaseItem.objects.filter(
                    product=OuterRef('pk'),
                    doc_purchase_id=party
                ).values('quantity')[:1]
            )
        )

        serializer = serializers.ProductListSerializer(qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class WarehouseProductListAPIView(APIView):
    def get(self, request):
        qs = document_models.Warehouse.objects.select_related('product', "created_by", "modified_by").filter(
            quantity__gt=0)
        waybill = self.request.query_params.get('waybill', None)
        category = self.request.query_params.get('category', None)

        if waybill:
            doc = document_models.DocOrder.objects.filter(waybill_number=waybill)
            if doc.exists():
                first_doc = doc.first()
                waybill_items = document_models.DocOrderItem.objects.filter(doc_order=first_doc)
                items = [item.product.id for item in waybill_items]
                qs = qs.filter(id__in=items).annotate(
                    order_item_quantity=Subquery(
                        document_models.DocOrderItem.objects.filter(
                            product=OuterRef('pk'),
                            doc_order_id=first_doc.id
                        ).values('quantity')[:1]
                    )
                )

        if category:
            qs = qs.filter(product__category__id=category)

        serializer = serializers.WarehouseListSerializer(qs, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
