from django.contrib import admin

import src.documents.models as models


class BaseModelAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ("id",)


@admin.register(models.Warehouse)
class WarehouseAdmin(BaseModelAdmin):
    search_fields = ("id", "product__name")
    list_display_links = ("id", "product")
    list_display = ("id", "product", "category", "quantity", "sell_price")
    list_editable = ("category", "quantity", "sell_price")


@admin.register(models.DocPurchase)
class DocPurchaseAdmin(BaseModelAdmin):
    list_filter = ("added_at",)
    list_display_links = ("id", "supplier")
    list_display = ("id", "supplier", "added_at")


@admin.register(models.DocPurchaseItem)
class DocPurchaseItemAdmin(BaseModelAdmin):
    list_editable = ("category",)
    list_filter = ("added_at", "category")
    list_display_links = ("id", "doc_purchase")
    list_display = ("id", "doc_purchase", "category", "product", "quantity", "purchase_price")


@admin.register(models.DocPurchaseReturn)
class DocPurchaseReturnAdmin(BaseModelAdmin):
    pass


@admin.register(models.DocPurchaseReturnItem)
class DocPurchaseReturnItemAdmin(BaseModelAdmin):
    pass


@admin.register(models.ProductResidual)
class ProductResidualAdmin(BaseModelAdmin):
    list_filter = ("product",)
    list_display_links = ("id", "party")
    list_display = ("id", "party", "product", "quantity")


@admin.register(models.DocOrder)
class DocOrderAdmin(BaseModelAdmin):
    list_display = ("id", "waybill_number", "customer", "added_at")
    list_display_links = ("id", "waybill_number")


@admin.register(models.DocOrderItem)
class DocOrderItemAdmin(BaseModelAdmin):
    list_display = ("id", "doc_order", "category", "product", "quantity", "added_at")
    list_display_links = ("id", "doc_order")
    list_editable = ("category",)


@admin.register(models.DocOrderReturn)
class DocOrderReturnAdmin(BaseModelAdmin):
    list_display = ("id", "doc_order", "status", "added_at")
    list_display_links = ("id", "doc_order")


@admin.register(models.DocOrderReturnItem)
class DocOrderReturnItemAdmin(BaseModelAdmin):
    pass
