from django.contrib import messages
from django.views.generic import ListView
from django_filters.views import FilterView
from django.shortcuts import render, redirect

from django.db import transaction

import src.core.models as models
import src.apps.core.forms as forms
import src.apps.core.filters as filters
import src.documents.models as document_models


class OrganizationPaymentsListView(FilterView, ListView):
    model = models.OrganizationPaymentHistory
    paginate_by = 15
    filterset_class = filters.OrganizationPaymentFilter
    template_name = "pages/payments/organization/list.html"


def create_organization_payment_history(request):
    if request.method == 'POST':
        form = forms.OrganizationPaymentHistoryForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.created_by = request.user
                payment.payment_type = models.CONSTANTS.PAYMENT_TYPE.payment
                doc = document_models.DocPurchase.objects.get(pk=payment.doc_purchase.id)
                doc.paid_amount += payment.amount
                doc.save()

                debt = models.OrganizationDebt.objects.last()
                debt.debt_amount -= payment.amount
                debt.save()
                payment.save()
                messages.success(request, "To'lov qo'shildi")
                return redirect("/payments/organization/list")
        else:
            messages.error(request, form.errors)
    else:
        form = forms.OrganizationPaymentHistoryForm()
    return render(request, "pages/payments/organization/form.html", {"form": form})


def update_organization_payment_history(request, pk):
    old_payment = models.OrganizationPaymentHistory.objects.get(pk=pk)
    old_amount = old_payment.amount

    if request.method == 'POST':
        form = forms.OrganizationPaymentHistoryForm(request.POST, instance=old_payment)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.modified_by = request.user
                payment.payment_type = models.CONSTANTS.PAYMENT_TYPE.payment

                amount_difference = payment.amount - old_amount

                doc = document_models.DocPurchase.objects.get(pk=payment.doc_purchase.id)
                doc.paid_amount += amount_difference
                doc.save()

                debt = models.OrganizationDebt.objects.last()
                debt.debt_amount -= amount_difference
                debt.save()

                payment.save()
                messages.success(request, "To'lov yangilandi")
                return redirect("/payments/organization/list")
        else:
            messages.error(request, form.errors)
    else:
        form = forms.OrganizationPaymentHistoryForm(instance=old_payment)
    return render(request, "pages/payments/organization/form.html", {"form": form, "payment": old_payment})
