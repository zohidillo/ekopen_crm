from django import forms
import src.core.models as models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'category', 'measurement']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'measurement': forms.Select(attrs={'class': 'form-control'}),
        }

