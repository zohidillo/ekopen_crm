from random import choices

import src.documents.models as models
import src.core.models as core_models

import django_filters
from django.forms import TextInput, Select, DateInput


class SaleFilter(django_filters.FilterSet):
    waybill_number = django_filters.CharFilter(
        field_name='waybill_number', label='Yuk xati raqami',
        widget=TextInput(attrs={'placeholder': 'YX-XXXX', 'class': 'form-control', "value": "YX-"})
    )

    customer = django_filters.ModelChoiceFilter(
        queryset=core_models.Customer.objects.all(),
        field_name='customer',
        label='Haridor',
        empty_label='Haridorni tanlang',
        widget=Select(attrs={'class': 'form-control'})
    )

    payment_method = django_filters.ChoiceFilter(
        field_name='payment_method',
        choices=core_models.CONSTANTS.DOC_ORDER_PAYMENT_METHOD.CHOICES,
        widget=Select(attrs={'class': 'form-control'})
    )

    payment_status = django_filters.ChoiceFilter(
        field_name='payment_status',
        choices=core_models.CONSTANTS.DOC_ORDER_PAYMENT_STATUS.CHOICES,
        widget=Select(attrs={'class': 'form-control'})
    )

    status = django_filters.ChoiceFilter(
        lookup_expr='icontains', label='Holati',
        choices=core_models.CONSTANTS.DOC_ORDER_STATUS.CHOICES,
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
        model = models.DocOrder
        fields = (
            "waybill_number", "customer", "status", "payment_method",
            "payment_status", "added_at__gte", "added_at__lte"
        )
