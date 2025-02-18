from django.db import transaction
from django.contrib import messages
from django_filters.views import FilterView
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.forms.models import modelformset_factory

from decimal import Decimal
from django.conf import settings
import src.documents.models as models
import src.apps.documents.filters as filters
from django.templatetags.static import static
from src.apps.documents.forms.sale.order import *


class SaleOrderListView(FilterView, ListView):
    model = models.DocOrder
    paginate_by = 15
    filterset_class = filters.SaleFilter
    template_name = "pages/documents/order/list.html"


@transaction.atomic
def create_order(request):
    doc_order_item_formset = modelformset_factory(models.DocOrderItem, form=DocOrderItemForm, extra=0)

    if request.method == 'POST':
        doc_order_form = DocOrderForm(request.POST)
        formset = doc_order_item_formset(request.POST)

        if doc_order_form.is_valid() and formset.is_valid():
            doc_order = doc_order_form.save(commit=False)
            doc_order.created_by = request.user
            doc_order.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    doc_order_item = form.save(commit=False)
                    doc_order_item.doc_order = doc_order
                    doc_order_item.created_by = request.user
                    doc_order_item.save()

            doc = models.DocOrder.objects.get(pk=doc_order.pk)
            doc.calculate_total_sum()
            doc.save()
            messages.success(request, 'Hisoblandi')
            return redirect(f"/document/sales/update/{doc_order.id}")

        else:
            if doc_order_form.errors:
                messages.error(request, f'order error: {doc_order_form.errors}')
            else:
                messages.error(request, f'order item error: {formset.errors}')
    else:
        doc_order_form = DocOrderForm()
        formset = doc_order_item_formset(queryset=models.DocOrderItem.objects.none())

    return render(request, "pages/documents/order/form.html", {
        "doc_order_form": doc_order_form,
        "formset": formset, "status": "create"
    })


@transaction.atomic
def update_order(request, pk):
    doc_order = models.DocOrder.objects.get(pk=pk)
    doc_order_item_formset = modelformset_factory(models.DocOrderItem, form=DocOrderItemForm, can_delete=True, extra=0)

    if request.method == 'POST':
        doc_order_form = DocOrderForm(request.POST, instance=doc_order)
        formset = doc_order_item_formset(request.POST, queryset=models.DocOrderItem.objects.filter(doc_order=doc_order))
        total_form_count = formset.total_form_count()
        print(formset.data)
        if doc_order_form.is_valid() and formset.is_valid():
            doc_order = doc_order_form.save(commit=False)
            doc_order.modified_by = request.user
            doc_order.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    quantity = form.cleaned_data.get('quantity')
                    product = form.cleaned_data.get('product')
                    if product:
                        doc_order_item = form.save(commit=False)
                        doc_order_item.doc_order = doc_order
                        doc_order_item.quantity = quantity
                        doc_order_item.modified_by = request.user
                        doc_order_item.save()

            # Yangi umumiy summani hisoblash
            doc = models.DocOrder.objects.get(pk=doc_order.pk)
            doc.calculate_total_sum()
            doc.save()
            if doc.status == "completed":
                messages.success(request, 'Malumotlatlar saqlandi')
                return redirect(f"/document/sales/list")
            else:
                messages.success(request, 'Malumotlatlar saqlandi')
                return redirect(f"/document/sales/update/{doc_order.id}")

        else:
            if doc_order_form.errors:
                messages.error(request, f'order error: {doc_order_form.errors}')
            else:
                messages.error(request, f'order item error: {formset.errors}')
    else:
        doc_order_form = DocOrderForm(instance=doc_order)
        formset = doc_order_item_formset(queryset=models.DocOrderItem.objects.filter(doc_order=doc_order))
        total_form_count = formset.total_form_count()

    return render(request, "pages/documents/order/form.html", {
        "doc_order_form": doc_order_form,
        "formset": formset, "total_form_count": total_form_count,
        "doc_order": doc_order, "status": "update"
    })


def waybill(request, pk):
    order = models.DocOrder.objects.get(pk=pk)
    order_items = order.items.select_related('product__product__category')

    category_totals = {}
    for item in order_items:
        category_name = item.product.product.category.name
        sale_sum = item.sale_sum
        if not category_totals.get(category_name):
            category_totals[category_name] = sale_sum
        else:
            category_totals[category_name] += sale_sum
    logo_url = request.build_absolute_uri(static('images/logo.jpg'))
    context = {
        'order': order,
        "logo_url": logo_url,
        "BASE_DIR": settings.BASE_DIR,
        'customer': order.customer,
        'category_totals': category_totals,
        'total_sum': f"{order.total_sum:,.2f}" if order.total_sum else 0,
        'paid_amount': f"{order.paid_amount:,.2f}" if order.paid_amount else 0,
        'order_items': order.items.all().order_by('category'),
        'remaining_debt': f"{order.remaining_balance:,.2f}" if order.remaining_balance else 0,
        "total_debt": f"{order.customer.debts.all().first().total_debt:,.2f}",
    }
    return render(request, "docs/waybill.html", context)
