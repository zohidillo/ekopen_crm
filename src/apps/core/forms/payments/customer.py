from django import forms

import src.core.models as models


class CustomerPaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = models.PaymentHistory
        fields = ("id", "customer", "doc_order", "amount", "old_debt")

        widgets = {
            "id": forms.HiddenInput(),
            "customer": forms.Select(attrs={"class": "form-control mb-3"}),
            "doc_order": forms.Select(attrs={"class": "form-control mb-3"}),
            "amount": forms.NumberInput(attrs={"class": "form-control mb-3"}),
            "old_debt": forms.CheckboxInput(attrs={"class": "form-check-input mx-2"}),
        }

