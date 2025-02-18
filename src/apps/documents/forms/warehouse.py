from django import forms

import src.documents.models as models


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = models.Warehouse
        fields = ["product", "quantity", "sell_price"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control", "disabled": "disabled"}),
            "quantity": forms.TextInput(attrs={"class": "form-control", "disabled": "disabled"}),
            "sell_price": forms.TextInput(attrs={"class": "form-control"}),
        }
