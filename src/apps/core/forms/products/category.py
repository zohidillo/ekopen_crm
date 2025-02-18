from django import forms
import src.core.models as models


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = models.ProductCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
