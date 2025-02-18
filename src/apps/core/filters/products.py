import src.documents.models as models
import src.core.models as core_models

import django_filters
from django.forms import TextInput, NumberInput, Select


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains', field_name='name', label='Qidirish',
        widget=TextInput(attrs={'class': "form-control"})
    )
    category = django_filters.ModelChoiceFilter(
        queryset=core_models.ProductCategory.objects.all(),
        field_name='category',
        label='Category',
        empty_label='Kategoryani tanlang',
        widget=Select(attrs={'class': "form-control"})
    )
    measurement = django_filters.ModelChoiceFilter(
        queryset=core_models.ProductMeasurement.objects.all(),
        field_name='measurement',
        label='Measurement',
        empty_label='O\'lchov birligni tanlang',
        widget=Select(attrs={'class': "form-control"})
    )

    class Meta:
        model = core_models.Product
        fields = ("name", "category", "measurement")
