from django.contrib import admin

import src.core.models as models


@admin.register(models.CustomerDebt)
class CustomerDebtAdmin(admin.ModelAdmin):
    search_fields = ("id",)
    list_editable = ("total_debt",)
    list_filter = ("added_at", "customer")
    list_display = ("id", "customer", "total_debt")


@admin.register(models.PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display_links = ("id", "customer",)
    list_filter = ("customer", "payment_type", "old_debt")
    list_display = ("id", "customer", "doc_order", "amount", "payment_type")


@admin.register(models.OrganizationDebt)
class OrganizationDebtAdmin(admin.ModelAdmin):
    list_display = ("id", "debt_amount")
    list_editable = ("debt_amount",)


@admin.register(models.OrganizationPaymentHistory)
class OrganizationPaymentHistoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = ("payment_type", "added_at")
    list_display_links = ("id", "doc_purchase",)
    list_display = ("id", "doc_purchase", "amount", "payment_type")
