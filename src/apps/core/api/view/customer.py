from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet

from django.shortcuts import get_object_or_404
from django.db.models import OuterRef, Subquery, Q

import src.core.models as models
import src.documents.models as document_models
import src.apps.core.api.serializers as serializers
from src.core.models import CONSTANTS


class CustomerListAPIView(ListAPIView, GenericViewSet):
    queryset = models.Customer.objects.select_related("created_by", "modified_by")
    serializer_class = serializers.CustomerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone_number__icontains=search)
            )
        return qs


class CustomerDebtPaymentView(APIView):

    def post(self, request):
        data = request.data
        customer_id = data.get("customer")
        amount = data.get("amount")
        customer = get_object_or_404(models.Customer, pk=customer_id)
        orders = document_models.DocOrder.objects.select_related("customer").filter(
            customer=customer, status=CONSTANTS.DOC_ORDER_STATUS.completed
        ).exclude(payment_status=CONSTANTS.DOC_ORDER_PAYMENT_STATUS.paid)

        extra = 0
        for i in orders:
            balance = i.remaining_balance
            if balance == amount:
                i.paid_amount += amount
                # i.save()
                #
                # debt = models.CustomerDebt.objects.get(customer=customer)
                # debt.total_debt -= amount
                # debt.save()
                break
            elif balance < amount:
                extra = amount - balance
                print(f"Extra: {extra}")

        return Response(f"{customer.get_total_debt}")
