from django.db import transaction
from django.contrib import messages
from django.views.generic import ListView
from django_filters.views import FilterView
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from decimal import Decimal
import src.documents.models as models
import src.apps.documents.filters as filters
from src.apps.documents.forms.purchase.doc_purchase import DocPurchaseForm, DocPurchaseItemForm


class DocPurchaseListView(FilterView, ListView):
    model = models.DocPurchase
    paginate_by = 15
    filterset_class = filters.DocumentPurchaseFilter
    template_name = "pages/documents/purchase/list.html"


@transaction.atomic
def create_doc_purchase(request):
    doc_purchase_item_form_set = modelformset_factory(models.DocPurchaseItem, form=DocPurchaseItemForm, extra=0,
                                                      can_delete=True)

    if request.method == 'POST':
        doc_purchase_form = DocPurchaseForm(request.POST)
        formset = doc_purchase_item_form_set(request.POST)
        if doc_purchase_form.is_valid() and formset.is_valid():
            doc_purchase = doc_purchase_form.save(commit=False)
            doc_purchase.created_by = request.user
            doc_purchase.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    product_id = form.cleaned_data.get('product')
                    quantity = form.cleaned_data.get('quantity')
                    purchase_price = form.cleaned_data.get('purchase_price')
                    if product_id:
                        doc_purchase_item = form.save(commit=False)
                        doc_purchase_item.doc_purchase = doc_purchase
                        doc_purchase_item.product = product_id
                        doc_purchase_item.quantity = quantity
                        doc_purchase_item.purchase_price = purchase_price
                        doc_purchase_item.created_by = doc_purchase.created_by
                        doc_purchase_item.save()

            messages.success(request, "Hammasi saqlandi")
            return redirect(f'/document/purchase/update/{doc_purchase.id}')
        else:
            if doc_purchase_form.errors:
                messages.error(request, f"Xato {doc_purchase_form.errors}")
            else:
                messages.error(request, f"Xato {formset.errors}")
    else:
        doc_purchase_form = DocPurchaseForm()
        formset = doc_purchase_item_form_set(queryset=models.DocPurchaseItem.objects.none())

    return render(request, 'pages/documents/purchase/form.html', {
        'doc_purchase_form': doc_purchase_form,
        'formset': formset,
    })


@transaction.atomic
def update_doc_purchase(request, pk):
    total_forms = 0
    doc_purchase = get_object_or_404(models.DocPurchase, pk=pk)
    doc_purchase_item_form_set = modelformset_factory(models.DocPurchaseItem, form=DocPurchaseItemForm, extra=0)

    if request.method == 'POST':
        doc_purchase_form = DocPurchaseForm(request.POST, instance=doc_purchase)
        formset = doc_purchase_item_form_set(request.POST, queryset=doc_purchase.items.all())

        if doc_purchase_form.is_valid() and formset.is_valid():
            doc_purchase = doc_purchase_form.save(commit=False)
            doc_purchase.created_by = request.user
            doc_purchase.save()

            total_forms = formset.total_form_count()
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    product_id = form.cleaned_data.get('product')
                    quantity = form.cleaned_data.get('quantity')
                    purchase_price = form.cleaned_data.get('purchase_price')
                    if product_id:
                        doc_purchase_item = form.save(commit=False)

                        doc_purchase_item.doc_purchase = doc_purchase
                        doc_purchase_item.product = product_id
                        doc_purchase_item.quantity = quantity
                        doc_purchase_item.purchase_price = purchase_price
                        doc_purchase_item.modified_by = doc_purchase.created_by
                        doc_purchase_item.save()

            doc_purchase.save()
            messages.success(request, "Hammasi saqlandi")
            return redirect(f'/document/purchase/update/{doc_purchase.id}')
        else:
            if doc_purchase_form.errors:
                messages.error(request, f"Xato {doc_purchase_form.errors}")
            else:
                messages.error(request, f"Xato {formset.errors}")
    else:
        doc_purchase_form = DocPurchaseForm(instance=doc_purchase)
        formset = doc_purchase_item_form_set(queryset=doc_purchase.items.all())
        total_forms = formset.total_form_count()

    return render(request, 'pages/documents/purchase/form.html', {
        'doc_purchase_form': doc_purchase_form,
        'formset': formset,
        'doc_purchase': doc_purchase,
        "status": "update", "total_form_count": total_forms,
    })
