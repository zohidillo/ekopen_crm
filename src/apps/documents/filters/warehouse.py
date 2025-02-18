import src.documents.models as models
import src.core.models as core_models

import django_filters
from django.forms import TextInput, NumberInput, Select


class WarehouseFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        lookup_expr='icontains', field_name='product__name', label='Qidirish',
        widget=TextInput(attrs={'placeholder': 'Qidirish', 'class': "form-control"})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=core_models.ProductCategory.objects.all(),
        field_name="category",
        label="Category",
        empty_label="Kategoryani tanlang",
        widget=Select(attrs={'class': 'form-control'})
    )

    min_quantity = django_filters.NumberFilter(
        field_name="quantity", lookup_expr='gte', label="Min Quantity",
        widget=NumberInput(attrs={'class': 'form-control'})
    )
    max_quantity = django_filters.NumberFilter(
        field_name="quantity", lookup_expr='lte', label="Max Quantity",
        widget=NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = models.Warehouse
        fields = ["search", 'category', 'min_quantity', 'max_quantity']
