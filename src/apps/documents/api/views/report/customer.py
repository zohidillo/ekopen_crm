from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone
from django.db.models.functions import TruncMonth, Coalesce, Concat, Round
from django.db.models import Q, F, Sum, Value, DecimalField, ExpressionWrapper

import src.core.models as core_models
import src.documents.models as document_models

date = timezone.now().date()
current_year = date.year


class TopCustomerReportView(APIView):
    def get(self, request, *args, **kwargs):
        total_quantity_sum = (
            document_models.DocOrderItem.objects
            .filter(doc_order__added_at__year=current_year)
            .aggregate(total=Coalesce(Sum("quantity"), Value(0), output_field=DecimalField()))["total"]
        )
        top_customers = (
            document_models.DocOrderItem.objects
            .filter(doc_order__added_at__year=current_year)
            .select_related("doc_order__customer")
            .values("doc_order__customer__first_name", "doc_order__customer__last_name")
            .annotate(
                full_name=Concat("doc_order__customer__first_name", Value(" "), "doc_order__customer__last_name"),
                total_quantity=Coalesce(Sum("quantity"), Value(0), output_field=DecimalField()),
                total_sum=Coalesce(Sum("sale_sum"), Value(0), output_field=DecimalField()),
                percentage=Coalesce(
                    Round(
                        ExpressionWrapper(
                            Sum("quantity") * Value(100.0) / Value(total_quantity_sum),
                            output_field=DecimalField(max_digits=5, decimal_places=2)
                        ),
                        2  # This will round the result to two decimal places
                    ),
                    Value(0.0),
                    output_field=DecimalField(max_digits=5, decimal_places=2)
                )
            )
            .order_by("full_name")
        )
        top_customers = list(top_customers)
        return Response(top_customers, status=status.HTTP_200_OK)
