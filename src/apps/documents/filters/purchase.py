import src.documents.models as models
import src.core.models as core_models

import django_filters
from django_filters.widgets import RangeWidget
from django.forms import TextInput, Select, DateInput


class DocumentPurchaseFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        lookup_expr='icontains', field_name='supplier', label='Qidirish',
        widget=TextInput(attrs={'placeholder': 'Qidirish', "class": "form-control"})
    )
    status = django_filters.ChoiceFilter(
        lookup_expr='icontains', label='Holati',
        choices=core_models.CONSTANTS.DOC_PURCHASE_STATUS.CHOICES,
        widget=Select(attrs={"class": "form-control"})
    )

    added_at__gte = django_filters.DateFilter(
        field_name='added_at', lookup_expr='gte', label="Boshlanish sanasi",
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    added_at__lte = django_filters.DateFilter(
        field_name='added_at', lookup_expr='lte', label="Tugash sanasi",
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = models.DocPurchase
        fields = ["search", "status", "added_at__gte", "added_at__lte"]
