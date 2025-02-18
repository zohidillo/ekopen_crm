from django import forms

import src.documents.models as models


class DocOrderForm(forms.ModelForm):
    class Meta:
        model = models.DocOrder
        fields = ("customer", "status", "payment_method", "paid_amount", "due_date")
        widgets = {
            "customer": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "paid_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class DocOrderItemForm(forms.ModelForm):
    class Meta:
        model = models.DocOrderItem
        fields = ("product", "quantity")
        widgets = {
            "id": forms.HiddenInput(),
            "product": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(DocOrderItemForm, self).__init__(*args, **kwargs)
        self.fields["product"].queryset = models.Warehouse.objects.select_related("product").filter(quantity__gt=0)
