from django import forms
import src.core.models as models


class ProductMeasurementForm(forms.ModelForm):
    class Meta:
        model = models.ProductMeasurement
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
