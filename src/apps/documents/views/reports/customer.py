from django.shortcuts import render

from django.utils import timezone
import src.documents.models as models
import src.core.models as core_models
from django.db.models.functions import TruncMonth, Coalesce, Concat, Round
from django.db.models import Q, F, Sum, Value, DecimalField, ExpressionWrapper

date = timezone.now().today()


def report_customer(request):
    current_year = date.year
    total_debts = core_models.CustomerDebt.objects.aggregate(
        total_debt_price=Sum('total_debt', output_field=DecimalField()))['total_debt_price']
    customers = core_models.Customer.objects.annotate(
        total_debt=Sum('debts__total_debt'),
        percentage=Coalesce(
            Round(
                ExpressionWrapper(
                    F("total_debt") * Value(100.0) / Value(total_debts),
                    output_field=DecimalField(max_digits=5, decimal_places=2)
                ),
                2
            ),
            Value(0.0),
            output_field=DecimalField(max_digits=5, decimal_places=2)
        )

    ).order_by('-total_debt')
    total_quantity_sum = (
        models.DocOrderItem.objects
        .filter(doc_order__added_at__year=current_year)
        .aggregate(total=Coalesce(Sum("quantity"), Value(0), output_field=DecimalField()))["total"]
    )
    top_customers = (
        models.DocOrderItem.objects
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
        .order_by("-total_quantity")
    )
    context = {
        "top_customers": list(top_customers),
        "debt_customers": customers
    }
    return render(request, "pages/reports/customer.html", context)
