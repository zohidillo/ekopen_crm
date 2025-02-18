from django.urls import path

import src.apps.documents.views.purchase.doc_purchase_return as views

urlpatterns = [
    path("create", views.create_doc_purchase_return, name="doc_purchase_return_create"),
    path("list", views.ListDocPurchaseReturn.as_view(), name="doc_purchase_return_list"),
    path("update/<int:pk>", views.update_doc_purchase_return, name="doc_purchase_return_update"),
]
