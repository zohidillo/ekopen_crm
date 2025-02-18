from django.shortcuts import render

from django.utils import timezone
import src.documents.models as models
import src.core.models as core_models
from django.db.models import Sum, Q, F, Count
from django.db.models.functions import TruncMonth

date = timezone.now().today()


def get_quarter_data(data: models.DocOrder, key):
    quarter = (date.month - 1) // 3 + 1

    if quarter == 1:
        start_date = date.replace(month=1, day=1)
        end_date = date.replace(month=3, day=31)
    elif quarter == 2:
        start_date = date.replace(month=4, day=1)
        end_date = date.replace(month=6, day=30)
    elif quarter == 3:
        start_date = date.replace(month=7, day=1)
        end_date = date.replace(month=9, day=30)
    else:
        start_date = date.replace(month=10, day=1)
        end_date = date.replace(month=12, day=31)

    a = data.filter(added_at__date__range=(start_date, end_date)).aggregate(amount=Sum(f"{key}"))["amount"]
    return a


purchase_report = (
    models.DocPurchaseItem.objects
    .filter(purchase_sum__gt=0, added_at__year=date.year)
    .annotate(month=TruncMonth('added_at'))
    .values('month')
    .annotate(total_purchase_quantity=Sum('quantity'), total_purchase=Sum("purchase_sum"))
    .order_by('month')
)

sales_report = (
    models.DocOrderItem.objects
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


def report_sale(request):
    doc_order = models.DocOrder.objects

    sale_year = doc_order.filter(added_at__year=date.year).aggregate(sale_sum_y=Sum("total_sum"))["sale_sum_y"]
    sale_month = doc_order.filter(
        added_at__year=date.year, added_at__month=date.month).aggregate(sale_sum_m=Sum("total_sum"))["sale_sum_m"]
    sale_quarter = get_quarter_data(doc_order, "total_sum")

    doc_order_item = models.DocOrderItem.objects
    sale_quantity_year = doc_order_item.filter(
        doc_order__added_at__year=date.year).aggregate(total_y=Sum("quantity"))["total_y"]
    sale_quantity_month = doc_order_item.filter(
        doc_order__added_at__year=date.year,
        doc_order__added_at__month=date.month).aggregate(total_m=Sum("quantity"))["total_m"]
    sale_quantity_quarter = get_quarter_data(doc_order_item, "quantity")

    total_report = {
        "sale_year": f"{sale_year:,.2f}" if sale_year else 0.00,
        "sale_month": f"{sale_month:,.2f}" if sale_month else 0.00,
        "sale_quarter": f"{sale_quarter:,.2f}" if sale_quarter else 0.00,

        "sale_quantity_year": f"{sale_quantity_year:,.2f}" if sale_quantity_year else 0.00,
        "sale_quantity_month": f"{sale_quantity_month:,.2f}" if sale_quantity_month else 0.00,
        "sale_quantity_quarter": f"{sale_quantity_quarter:,.2f}" if sale_quantity_quarter else 0.00,
    }

    customers = core_models.Customer.objects.annotate(
        total_sale_sum=Sum("doc_orders__total_sum",
                           filter=Q(doc_orders__added_at__year=date.year)),
        total_paid_sum=Sum("doc_orders__paid_amount",
                           filter=Q(doc_orders__added_at__year=date.year)),
        total_debt_sum=F("total_sale_sum") - F("total_paid_sum"),
        total_debt_percent=(F("total_debt_sum") * 100) / F("total_sale_sum")
    ).order_by("id")

    customer_report = {
        "customers": customers,
    }

    categories = core_models.ProductCategory.objects.all()
    result = []

    for category in categories:
        purchase_data = models.DocPurchaseItem.objects.select_related("category").filter(
            category=category,
            added_at__year=date.year
        ).aggregate(
            total_quantity=Sum('quantity'),
            total_cost=Sum(F('quantity') * F('purchase_price'))
        )
        total_purchase_count = purchase_data['total_quantity'] or 0
        purchase_total = purchase_data['total_cost'] or 0

        sold_data = models.DocOrderItem.objects.select_related("category").filter(
            category=category,
            added_at__year=date.year
        ).aggregate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('quantity') * F('sale_price'))
        )
        total_sold_count = sold_data['total_quantity'] or 0
        sold_total = sold_data['total_revenue'] or 0

        in_warehouse = models.Warehouse.objects.select_related("category").filter(
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
            'sold_percent': sold_percent,
            'purchase_total': f"{purchase_total:,.2f}" if purchase_total else 0.00,
            'sold_total': f"{sold_total:,.2f}" if sold_total else 0.00
        })

    category_report = {
        "year": date.year,
        "category": result,
        "month_report": combined_report
    }

    context = total_report | customer_report | category_report
    return render(request, "pages/reports/sales.html", context=context)
