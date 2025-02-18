from django.views.generic import ListView
from django_filters.views import FilterView
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
import src.documents.models as models
import src.apps.documents.filters as filters
from src.apps.documents.forms.warehouse import WarehouseForm


class WarehouseListView(FilterView, ListView):
    model = models.Warehouse
    paginate_by = 15
    filterset_class = filters.WarehouseFilter
    template_name = "pages/documents/warehouse/list.html"


def update_warehouse(request, pk):
    warehouse = get_object_or_404(models.Warehouse, id=pk)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.modified_by = request.user
            obj.save()
            messages.success(request, 'Saqlandi')
            return redirect(f'/document/warehouse/update/{pk}')
        else:
            messages.success(request, f'Xato: {form.errors}')
    else:
        form = WarehouseForm(instance=warehouse)

    return render(request, 'pages/documents/warehouse/form.html', {'form': form, 'warehouse': warehouse})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_quantity(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sell_price = data.get('sell_price', 0)
            obj = models.Warehouse.objects.get(pk=pk)
            obj.sell_price = sell_price
            obj.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
