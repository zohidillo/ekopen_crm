from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone
from django.db.models import Q, F, Sum
from django.db.models.functions import TruncMonth

import src.core.models as core_models
import src.documents.models as document_models


class SaleReportCategoryAPIView(APIView):
    def get(self, request):
        date = timezone.now().date()
        categories = core_models.ProductCategory.objects.all()
        result = []

        for category in categories:
            purchase_data = document_models.DocPurchaseItem.objects.select_related("category").filter(
                category=category,
                added_at__year=date.year
            ).aggregate(
                total_quantity=Sum('quantity'),
                total_cost=Sum(F('quantity') * F('purchase_price'))
            )
            total_purchase_count = purchase_data['total_quantity'] or 0
            purchase_total = purchase_data['total_cost'] or 0

            sold_data = document_models.DocOrderItem.objects.select_related("category").filter(
                category=category,
                added_at__year=date.year
            ).aggregate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum(F('quantity') * F('sale_price'))
            )
            total_sold_count = sold_data['total_quantity'] or 0
            sold_total = sold_data['total_revenue'] or 0

            in_warehouse = document_models.Warehouse.objects.select_related("category").filter(
                category=category,
                added_at__year=date.year
            ).aggregate(total_quantity=Sum('quantity'), total_price=Sum(F("quantity") * F("sell_price")))

            in_warehouse_count = in_warehouse['total_quantity'] or 0
            in_warehouse_total = in_warehouse['total_price'] or 0

            sold_percent = ((total_sold_count * 100) / total_purchase_count) if total_purchase_count else 0

            result.append({
                'name': category.name,
                'total_purchase_count': f"{total_purchase_count:,.2f}" if total_purchase_count else 0,
                'total_sold_count': f"{total_sold_count:,.2f}" if total_sold_count else 0,
                'in_warehouse_count': f"{in_warehouse_count:,.2f}" if in_warehouse_count else 0,
                'in_warehouse_price': f"{in_warehouse_total:,.2f}" if in_warehouse_total else 0,
                'sold_percent': f"{sold_percent:,.2f}" if sold_percent else 0,
                'purchase_total': f"{purchase_total:,.2f}" if purchase_total else 0,
                'sold_total': f"{sold_total:,.2f}" if sold_total else 0
            })

        return Response(result, status=status.HTTP_200_OK)


class MonthSalesReportAPIView(APIView):
    def get(self, request):
        date = timezone.now().date()

        purchase_report = (
            document_models.DocPurchaseItem.objects
            .filter(purchase_sum__gt=0, added_at__year=date.year)
            .annotate(month=TruncMonth('added_at'))
            .values('month')
            .annotate(total_purchase_quantity=Sum('quantity'), total_purchase=Sum("purchase_sum"))
            .order_by('month')
        )

        sales_report = (
            document_models.DocOrderItem.objects
            .filter(sale_sum__gt=0, added_at__year=date.year)
            .annotate(month=TruncMonth('added_at'))
            .values('month')
            .annotate(total_sale_quantity=Sum('quantity'), total_sale=Sum("sale_sum"))
            .order_by('month')
        )

        purchase_dict = {item['month']: item for item in purchase_report}
        sales_dict = {item['month']: item for item in sales_report}

        all_months = sorted(set(purchase_dict.keys()).union(sales_dict.keys()))
        combined_report = []

        for month in all_months:
            combined_report.append({
                'month': 'Unknown' if not month else month.strftime('%B'),
                'total_purchase_quantity': purchase_dict.get(month, {}).get('total_purchase_quantity', 0),
                'total_purchase': purchase_dict.get(month, {}).get('total_purchase', 0),
                'total_sale_quantity': sales_dict.get(month, {}).get('total_sale_quantity', 0),
                'total_sale': sales_dict.get(month, {}).get('total_sale', 0),
            })

        return Response(combined_report, status.HTTP_200_OK)
