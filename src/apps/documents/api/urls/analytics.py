from django.urls import path

import src.apps.documents.api.views.analytics as view

urlpatterns = [
    path("yearly_sale_data/", view.YearlySaleDataView.as_view()),
    path("monthly_sale_data/", view.MonthlySaleDataView.as_view())
]
