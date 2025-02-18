from django.contrib import messages
from django.views.generic import ListView
from django_filters.views import FilterView
from django.shortcuts import render, redirect

from django.db import transaction

import src.core.models as models
import src.apps.core.forms as forms
import src.apps.core.filters as filters
import src.documents.models as document_models


class CustomerPaymentsListView(FilterView, ListView):
    model = models.PaymentHistory
    paginate_by = 15
    filterset_class = filters.PaymentFilter
    template_name = "pages/payments/customer/list.html"


def create_payment_history(request):
    if request.method == "POST":
        form = forms.CustomerPaymentHistoryForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                payment = form.save(commit=False)
                payment.created_by = request.user
                payment.payment_type = "payment"
                if payment.old_debt:
                    debt = models.CustomerDebt.objects.get(customer=payment.customer)
                    debt.total_debt -= payment.amount
                    debt.save()
                elif payment.doc_order:
                    doc = document_models.DocOrder.objects.get(pk=payment.doc_order.id)
                    doc.paid_amount += payment.amount
                    doc.save()

                    debt = models.CustomerDebt.objects.get(customer=payment.customer)
                    debt.total_debt -= payment.amount
                    debt.save()
                payment.save()

                messages.success(request, "To'lov qo'shildi")
                return redirect("/payments/customer/list")
        else:
            messages.error(request, form.errors)
    else:
        form = forms.CustomerPaymentHistoryForm()
    return render(request, "pages/payments/customer/form.html", {"form": form})


def update_payment_history(request, pk):
    old_payment = models.PaymentHistory.objects.get(pk=pk)
    old_amount = old_payment.amount  # Store the old amount for comparison

    if request.method == "POST":
        form = forms.CustomerPaymentHistoryForm(request.POST, instance=old_payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.modified_by = request.user

            # Calculate the amount difference
            amount_difference = payment.amount - old_amount

            if payment.old_debt:
                debt = models.CustomerDebt.objects.get(customer=payment.customer)
                debt.total_debt -= amount_difference  # Adjust total debt based on difference
                debt.save()
            elif payment.doc_order:
                doc = document_models.DocOrder.objects.get(pk=payment.doc_order.id)
                doc.paid_amount += amount_difference  # Adjust paid amount based on difference
                doc.save()

                debt = models.CustomerDebt.objects.get(customer=payment.customer)
                debt.total_debt -= amount_difference  # Adjust total debt again
                debt.save()

            payment.save()
            messages.success(request, "To'lov yangilandi")
            return redirect("/payments/customer/list")
        else:
            messages.error(request, form.errors)
    else:
        form = forms.CustomerPaymentHistoryForm(instance=old_payment)

    return render(request, "pages/payments/customer/form.html", {"form": form, "payment": old_payment})
