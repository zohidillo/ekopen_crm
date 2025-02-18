from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404

import src.apps.core.forms as forms
import src.core.models as models


class CategoryListView(ListView):
    model = models.ProductCategory
    paginate_by = 15
    template_name = "pages/products/category/category.html"


def create_product_category(request):
    if request.method == 'POST':
        form = forms.ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product category created successfully!')
            return redirect('category-list')  # Muvaffaqiyatli yaratishdan keyin yo'naltirish
    else:
        form = forms.ProductCategoryForm()

    return render(request, 'pages/products/category/add.html', {'form': form})


def update_product_category(request, pk):
    category = get_object_or_404(models.ProductCategory, pk=pk)
    if request.method == 'POST':
        form = forms.ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('category-list')
    else:
        form = forms.ProductCategoryForm(instance=category)

    return render(request, 'pages/products/category/add.html', {'form': form})
