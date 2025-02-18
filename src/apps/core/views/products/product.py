from django.contrib import messages
from django.views.generic import ListView
from django_filters.views import FilterView
from django.shortcuts import render, redirect, get_object_or_404

import src.core.models as models
import src.apps.core.forms as forms
import src.apps.core.filters as filters


class ProductListView(FilterView, ListView):
    model = models.Product
    paginate_by = 15
    filterset_class = filters.ProductFilter
    template_name = "pages/products/all_product/list.html"


def create_product(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully!")
            return redirect('/product/list')
    else:
        form = forms.ProductForm()

    return render(request, 'pages/products/all_product/form.html', {'form': form})


def update_product(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('/product/list')
    else:
        form = forms.ProductForm(instance=product)

    return render(request, 'pages/products/all_product/form.html', {'form': form})
