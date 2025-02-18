from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404

import src.apps.core.forms as forms
import src.core.models as models


class MeasurementListView(ListView):
    model = models.ProductMeasurement
    paginate_by = 15
    template_name = "pages/products/measurements/list.html"


def create_measurement(request):
    if request.method == 'POST':
        form = forms.ProductMeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Measurement category created successfully!')
            return redirect('measurement-list')  # Muvaffaqiyatli yaratishdan keyin yo'naltirish
    else:
        form = forms.ProductMeasurementForm()

    return render(request, 'pages/products/measurements/form.html', {'form': form})


def update_measurement(request, pk):
    instance = get_object_or_404(models.ProductMeasurement, pk=pk)
    if request.method == 'POST':
        form = forms.ProductMeasurementForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Measurement updated successfully!")
            return redirect('measurement-list')
    else:
        form = forms.ProductMeasurementForm(instance=instance)

    return render(request, 'pages/products/measurements/form.html', {'form': form})
