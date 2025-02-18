from django import forms

import src.core.models as models


class OrganizationPaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = models.OrganizationPaymentHistory
        fields = ("id", "doc_purchase", "amount")

        widgets = {
            "id": forms.HiddenInput(),
            "doc_purchase": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control mb-3"}),
        }
