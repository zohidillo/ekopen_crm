import django_filters
from django.db.models import Q
from django.forms import TextInput
from src.core.models import Customer


class CustomerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_all_fields',
        label='Qidirish',
        widget=TextInput(attrs={'placeholder': 'Ism, familiya yoki telefon', 'class': 'form-control'})
    )

    class Meta:
        model = Customer
        fields = ['search']

    def filter_by_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(phone_number__icontains=value)
        )
