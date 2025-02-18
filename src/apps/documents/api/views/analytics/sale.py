from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import calendar
from django.db.models import Sum
from django.utils import timezone

import src.documents.models as models


class YearlySaleDataView(APIView):
    def get(self, request):
        today = timezone.now().date()
        doc_orders = (
            models.DocOrder.objects
            .filter(added_at__year=today.year)
            .values('added_at__month')
            .annotate(total_sales=Sum('total_sum'), total_payments=Sum('paid_amount'))
            .order_by('added_at__month')
        )

        sales_data = {str(day): 0 for day in range(1, 12 + 1)}
        payments_data = {str(day): 0 for day in range(1, 12 + 1)}
        for sale in doc_orders:
            sales_data[str(sale['added_at__month'])] = float(sale['total_sales'])
            payments_data[str(sale['added_at__month'])] = float(sale['total_payments'])

        data = [
            {
                "months": ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr",
                           "Noyabr", "Dekabr"],
                "sales": sales_data.values(),
                "payments": payments_data.values(),
            }
        ]
        return Response(data, status=status.HTTP_200_OK)


class MonthlySaleDataView(APIView):
    def get(self, request):
        today = timezone.now().date()
        days = calendar.monthrange(today.year, today.month)[1]
        this_month_days = [f"{i}" for i in range(1, days + 1)]
        doc_orders = (
            models.DocOrder.objects
            .filter(added_at__month=today.month, added_at__year=today.year)
            .values('added_at__day')
            .annotate(total_sales=Sum('total_sum'), total_payments=Sum('paid_amount'))
            .order_by('added_at__day')
        )

        sales_data = {str(day): 0 for day in range(1, days + 1)}
        payments_data = {str(day): 0 for day in range(1, days + 1)}
        for sale in doc_orders:
            sales_data[str(sale['added_at__day'])] = float(sale['total_sales'])
            payments_data[str(sale['added_at__day'])] = float(sale['total_payments'])

        data = [
            {
                "days": this_month_days,
                "sales": sales_data.values(),
                "payments": payments_data.values()
            }

        ]
        return Response(data, status=status.HTTP_200_OK)
