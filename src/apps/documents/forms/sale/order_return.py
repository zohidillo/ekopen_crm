from django import forms

import src.documents.models as models


class DocOrderReturnForm(forms.ModelForm):
    waybill_number = forms.CharField(max_length=12, required=True)

    class Meta:
        model = models.DocOrderReturn
        fields = ("doc_order", "reason", "status")
        widgets = {
            "doc_order": forms.Select(attrs={"class": "form-control"}),  # waybill_number ga class berish
            "status": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
        }


class DocOrderReturnItemForm(forms.ModelForm):
    class Meta:
        model = models.DocOrderReturnItem
        fields = ("product", "quantity")
        widgets = {
            "id": forms.HiddenInput(),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }

