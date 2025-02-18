from django import forms
import src.documents.models as models


class DocPurchaseForm(forms.ModelForm):
    class Meta:
        model = models.DocPurchase
        fields = ('supplier', "paid_amount", "status")
        widgets = {
            'id': forms.HiddenInput(),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DocPurchaseItemForm(forms.ModelForm):
    class Meta:
        model = models.DocPurchaseItem
        fields = ('product', 'quantity', 'purchase_price')
        widgets = {
            'id': forms.HiddenInput(),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_price': forms.TextInput(attrs={'class': 'form-control'}),
        }
