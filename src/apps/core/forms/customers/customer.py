from django import forms

import src.core.models as models


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ("first_name", "last_name", "address", "phone_number")

        widgets = {
            "modified_by": forms.HiddenInput(),
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_number": forms.TextInput(attrs={'class': 'form-control'}),
        }
