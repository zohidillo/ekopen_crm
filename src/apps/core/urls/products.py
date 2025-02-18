from django.urls import path

import src.apps.core.views.products as views

urlpatterns = [
    path("list", views.ProductListView.as_view(), name="product-list"),
    path("create", views.create_product, name="product-create"),
    path("update/<int:pk>", views.update_product, name="product-update"),

    path("category/list", views.CategoryListView.as_view(), name="category-list"),
    path("category/create", views.create_product_category, name="category-create"),
    path("category/update/<int:pk>", views.update_product_category, name="category-update"),

    path("measurement/list", views.MeasurementListView.as_view(), name="measurement-list"),
    path("measurement/create", views.create_measurement, name="measurement-create"),
    path("measurement/update/<int:pk>", views.update_measurement, name="measurement-update"),

]
