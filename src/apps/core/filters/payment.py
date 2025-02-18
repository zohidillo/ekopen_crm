import src.documents.models as models
import src.core.models as core_models

import django_filters
from django.forms import TextInput, NumberInput, Select, DateInput


class PaymentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        lookup_expr='icontains', label='Qidirish', field_name='doc_order__waybill_number',
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'})
    )
    customer = django_filters.ModelChoiceFilter(
        queryset=core_models.Customer.objects.all(),
        field_name='customer',
        label='Haridorlar',
        empty_label='Haridorni tanlang',
        widget=Select(attrs={"class": "form-control"}),
    )
    payment_type = django_filters.ChoiceFilter(
        field_name='payment_type',
        choices=core_models.CONSTANTS.PAYMENT_TYPE.CHOICES,
        widget=Select(attrs={"class": "form-control"}),
    )
    old_debt = django_filters.BooleanFilter(
        field_name='old_debt',
        label='Eski qarz',
        widget=Select(attrs={'class': 'form-control'}, choices=[
            ('', 'Tanlang'),
            ('true', 'Ha'),
            ('false', 'Yo\'q'),
        ])
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
        model = core_models.PaymentHistory
        fields = ("search", "customer", 'payment_type', "old_debt", "added_at__gte", "added_at__lte")


class OrganizationPaymentFilter(django_filters.FilterSet):
    doc_purchase = django_filters.ModelChoiceFilter(
        queryset=models.DocPurchase.objects.all(),
        field_name='doc_purchase',
        label='Harid',
        empty_label='Haridni tanlang',
        widget=Select(attrs={"class": "form-control"}),
    )
    payment_type = django_filters.ChoiceFilter(
        field_name='payment_type',
        choices=core_models.CONSTANTS.PAYMENT_TYPE.CHOICES,
        widget=Select(attrs={"class": "form-control"}),
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
        model = core_models.OrganizationPaymentHistory
        fields = ("doc_purchase", "payment_type")
