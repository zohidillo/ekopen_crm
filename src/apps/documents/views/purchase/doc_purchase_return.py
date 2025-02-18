from django.db import transaction
from django.contrib import messages
from django.views.generic import ListView
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404

from decimal import Decimal
import src.documents.models as models
from src.apps.documents.forms.purchase.doc_purchase_return import DocPurchaseReturnForm, DocPurchaseReturnItemsForm
from src.documents.models import DocPurchaseReturn


class ListDocPurchaseReturn(ListView):
    model = DocPurchaseReturn
    paginate_by = 15
    template_name = "pages/documents/purchase_return/list.html"


@transaction.atomic
def create_doc_purchase_return(request):
    doc_purchase_return_item_formset = modelformset_factory(
        models.DocPurchaseReturnItem,
        form=DocPurchaseReturnItemsForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        doc_purchase_return_form = DocPurchaseReturnForm(request.POST)
        formset = doc_purchase_return_item_formset(request.POST, queryset=models.DocPurchaseReturnItem.objects.none())

        if doc_purchase_return_form.is_valid() and formset.is_valid():
            # Save DocPurchaseReturn instance
            doc_purchase_return = doc_purchase_return_form.save(commit=False)
            doc_purchase = doc_purchase_return_form.cleaned_data.get("doc_purchase")
            doc_purchase_return.created_by = request.user
            doc_purchase_return.doc_purchase = doc_purchase
            doc_purchase_return.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    item = form.save(commit=False)
                    product = form.cleaned_data.get('product')
                    new_quantity = form.cleaned_data.get('quantity')
                    if product:
                        returned_product = models.DocPurchaseItem.objects.filter(
                            doc_purchase=doc_purchase_return.doc_purchase,
                            product_id=product)
                        if returned_product.exists():
                            returned_product_first = returned_product.first()

                            item.purchase_price = returned_product_first.purchase_price
                            item.doc_purchase_return = doc_purchase_return
                            item.created_by = request.user
                            item.save()

            doc = models.DocPurchaseReturn.objects.get(id=doc_purchase_return.id)
            items = doc.items.all()
            total_purchase_sum = sum([item.purchase_sum for item in items])
            doc.total_purchase_sum = total_purchase_sum
            doc.calculate_return_amount()
            doc.save()

            messages.success(request, 'Malumotlar saqlandi')
            return redirect(f"/document/purchase-return/update/{doc_purchase_return.id}")
        else:
            if doc_purchase_return_form.errors:
                messages.error(request, f"Xato {doc_purchase_return_form.errors}")
            else:
                messages.error(request, f"Xato {formset.errors}")
    else:
        doc_purchase_return_form = DocPurchaseReturnForm()
        formset = doc_purchase_return_item_formset(queryset=models.DocPurchaseReturnItem.objects.none())

    return render(request, 'pages/documents/purchase_return/form.html', {
        'doc_purchase_return_form': doc_purchase_return_form,
        'formset': formset,
    })


@transaction.atomic
def update_doc_purchase_return(request, pk):
    # Mavjud qaytishni olish
    doc_purchase_return = get_object_or_404(models.DocPurchaseReturn, pk=pk)
    doc_purchase = doc_purchase_return.doc_purchase

    # Formset yaratish, doc_purchase_id ni uzatamiz
    doc_purchase_return_item_formset = modelformset_factory(models.DocPurchaseReturnItem,
                                                            form=DocPurchaseReturnItemsForm,
                                                            extra=0, can_delete=True)

    if request.method == 'POST':
        # Form va formsetni POST ma'lumotlari bilan to'ldirish
        doc_purchase_return_form = DocPurchaseReturnForm(request.POST, instance=doc_purchase_return)
        formset = doc_purchase_return_item_formset(request.POST, queryset=doc_purchase_return.items.all())

        if doc_purchase_return_form.is_valid() and formset.is_valid():
            doc_purchase_return = doc_purchase_return_form.save(commit=False)
            doc_purchase_return.modified_by = request.user
            doc_purchase_return.save()

            for form in formset:
                doc_purchase_return_item = form.save(commit=False)
                new_quantity = form.cleaned_data.get('quantity')
                product = form.cleaned_data.get('product')
                if product:
                    returned_product = models.DocPurchaseItem.objects.filter(doc_purchase=doc_purchase, product=product)
                    if returned_product.exists():
                        returned_product_first = returned_product.first()

                        doc_purchase_return_item.purchase_price = returned_product_first.purchase_price
                        doc_purchase_return_item.doc_purchase_return = doc_purchase_return
                        doc_purchase_return_item.purchase_sum = new_quantity * returned_product_first.purchase_price
                        doc_purchase_return_item.save()

            # To'liq summa va omborni yangilash
            doc = models.DocPurchaseReturn.objects.get(id=doc_purchase_return.id)
            items = doc.items.all()
            total_purchase_sum = sum([item.purchase_sum for item in items])
            doc.total_purchase_sum = total_purchase_sum
            doc.calculate_return_amount()
            doc.calculation()
            doc.save()

            messages.success(request, "Malumotlar saqlandi")
            return redirect(f'/document/purchase-return/update/{doc.id}')
        else:
            if doc_purchase_return_form.errors:
                messages.error(request, f"Xato {doc_purchase_return_form.errors}")
            else:
                messages.error(request, f"Xato {formset.errors}")
    else:
        doc_purchase_return_form = DocPurchaseReturnForm(instance=doc_purchase_return)
        formset = doc_purchase_return_item_formset(queryset=doc_purchase_return.items.all())

    return render(request, 'pages/documents/purchase_return/form.html', {
        'doc_purchase_return_form': doc_purchase_return_form,
        'formset': formset, "status": "update",
        "doc_purchase_return": doc_purchase_return
    })
