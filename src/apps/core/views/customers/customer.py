from django_filters.views import FilterView
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.db.models import Sum
import src.core.models as models
import src.apps.core.forms as forms
import src.apps.core.filters as filters


class CustomerListView(FilterView, ListView):
    model = models.Customer
    paginate_by = 15
    filterset_class = filters.CustomerFilter
    template_name = "pages/customers/customer/list.html"

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            total_debt=Sum('debts__total_debt')
        ).order_by('-total_debt')
        return qs


class CustomerDetailView(DetailView):
    model = models.Customer
    template_name = "pages/customers/customer/detail.html"


class CustomerCreateView(CreateView):
    model = models.Customer
    form_class = forms.CustomerForm
    template_name = "pages/customers/customer/forms.html"
    success_url = "/customers/list"


class CustomerUpdateView(UpdateView):
    model = models.Customer
    form_class = forms.CustomerForm
    template_name = "pages/customers/customer/forms.html"
    success_url = "/customers/list"
