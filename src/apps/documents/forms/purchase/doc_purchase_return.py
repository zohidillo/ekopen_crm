from django import forms

import src.core.models as core_models
import src.documents.models as models


class DocPurchaseReturnForm(forms.ModelForm):
    class Meta:
        model = models.DocPurchaseReturn
        fields = ("reason", "doc_purchase", "status")

        widgets = {
            "reason": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "doc_purchase": forms.Select(attrs={"class": "form-control"}),
        }


class DocPurchaseReturnItemsForm(forms.ModelForm):
    class Meta:
        model = models.DocPurchaseReturnItem
        fields = ("product", "quantity")

        widgets = {
            "id": forms.HiddenInput(),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"})
        }
