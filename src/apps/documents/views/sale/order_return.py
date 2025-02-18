from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.forms.models import modelformset_factory

from decimal import Decimal
from src.apps.documents.forms.sale.order_return import *


class ReturnOrderListView(ListView):
    model = models.DocOrderReturn
    paginate_by = 15
    template_name = "pages/documents/order-return/list.html"


@transaction.atomic
def create_order_return(request):
    # Create a formset for DocOrderReturnItem
    doc_order_return_item_formset = modelformset_factory(models.DocOrderReturnItem, form=DocOrderReturnItemForm,
                                                         can_delete=True, extra=0)

    if request.method == 'POST':
        order_form = DocOrderReturnForm(request.POST)
        formset = doc_order_return_item_formset(request.POST, queryset=models.DocOrderReturnItem.objects.none())

        if order_form.is_valid() and formset.is_valid():
            waybill_number = order_form.cleaned_data.pop("waybill_number")

            # Retrieve the related DocOrder by waybill_number
            doc = models.DocOrder.objects.filter(waybill_number=waybill_number)
            if doc.exists():
                first_doc = doc.first()

                # Save the DocOrderReturn instance
                doc_order_return = order_form.save(commit=False)
                doc_order_return.created_by = request.user
                doc_order_return.doc_order = first_doc
                doc_order_return.save()
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        item = form.save(commit=False)
                        item.return_order = doc_order_return
                        item.created_by = request.user
                        item.save()

                items = doc_order_return.items.all()
                total_sum = 0
                for item in items:
                    total_sum += item.sold_price_sum

                doc_order_return.total_sum = total_sum
                doc_order_return.calculate_return_amount()
                doc_order_return.save()
                messages.success(request, "Saqlandi")
                return redirect(f"/document/sales-return/update/{doc_order_return.id}")
            else:
                messages.error(request, "Buyurtma topilmadi")
        else:
            if order_form.errors:
                messages.error(request, f"Xato: form {order_form.errors}")
            else:
                messages.error(request, f"Xato formset {formset.errors}")
    else:
        # If GET, create an empty form and formset
        order_form = DocOrderReturnForm()
        formset = doc_order_return_item_formset(queryset=models.DocOrderReturnItem.objects.none())

    return render(request, 'pages/documents/order-return/form.html', {
        "return_order_form": order_form,
        "formset": formset,
        "status": "update"
    })


@transaction.atomic
def update_order_return(request, pk):
    return_order = models.DocOrderReturn.objects.get(id=pk)
    doc_order = models.DocOrder.objects.filter(id=return_order.doc_order.id).first()

    return_order_item_formset = modelformset_factory(
        models.DocOrderReturnItem,
        form=DocOrderReturnItemForm,
        extra=0,
        can_delete=True,
    )

    if request.method == 'POST':
        return_order_form = DocOrderReturnForm(request.POST, instance=return_order)
        formset = return_order_item_formset(
            request.POST,
            queryset=models.DocOrderReturnItem.objects.filter(return_order=return_order)
        )
        total_formset = formset.total_form_count()

        if return_order_form.is_valid() and formset.is_valid():
            waybill_number = return_order_form.cleaned_data.pop("waybill_number")
            doc_return = return_order_form.save(commit=False)
            doc_return.modified_by = request.user
            doc_return.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    quantity = form.cleaned_data.get("quantity")
                    product = form.cleaned_data.get("product")
                    if product:
                        return_item = form.save(commit=False)
                        return_item.return_order = return_order
                        return_item.modified_by = request.user
                        return_item.save()

            items = doc_return.items.all()
            total_sum = 0
            for item in items:
                total_sum += item.sold_price_sum

            doc_return.total_sum = total_sum
            doc_return.calculate_return_amount()
            doc_return.fix_amounts()
            doc_return.save()
            if doc_return.status == "completed":
                messages.success(request, "Malumotlar saqlandi")
                return redirect(f'/document/sales-return/update/{doc_return.id}')
            else:
                messages.success(request, "Malumotlar saqlandi")
                return redirect(f'/document/sales-return/update/{doc_return.id}')
        else:
            if return_order_form.errors:
                messages.error(request, f'return order error: {return_order_form.errors}')
            else:
                messages.error(request, f'return order item error: {formset.errors}')

    else:
        return_order_form = DocOrderReturnForm(instance=return_order)
        formset = return_order_item_formset(
            queryset=models.DocOrderReturnItem.objects.filter(return_order=return_order)
        )
        total_formset = formset.total_form_count()

    context = {
        'return_order_form': return_order_form,
        'formset': formset,
        'return_order': return_order,
        "status": "update", "total_formset": total_formset,
        "total_debt": return_order.doc_order.customer.get_total_debt
    }

    return render(request, 'pages/documents/order-return/form.html', context)
