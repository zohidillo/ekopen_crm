from django.urls import path

import src.apps.documents.views.purchase as views

urlpatterns = [
    path("create", views.create_doc_purchase, name="doc_purchase_create"),
    path("list", views.DocPurchaseListView.as_view(), name="doc_purchase_list"),
    path("update/<int:pk>", views.update_doc_purchase, name="doc_purchase_update"),
]
