from decimal import Decimal
from django.db import models
import src.core.models as core_models
from src.documents.models import Warehouse, DocPurchaseItem


class DocPurchaseReturn(core_models.BaseModel):
    reason = models.CharField(max_length=255, null=True, blank=True,
                              choices=core_models.CONSTANTS.DOC_PURCHASE_RETURN_REASON.CHOICES)
    status = models.CharField(max_length=255, null=True, blank=True,
                              choices=core_models.CONSTANTS.DOC_ORDER_RETURN_STATUS.CHOICES, default="pending")
    total_purchase_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    doc_purchase = models.ForeignKey("DocPurchase", on_delete=models.CASCADE, related_name="doc_return",
                                     null=True, blank=True)
    return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk} {self.reason} {self.added_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def get_reason(self):
        if self.reason == core_models.CONSTANTS.DOC_PURCHASE_RETURN_REASON.defective:
            return "Nuqsonli"

    @property
    def get_status(self):
        if self.status == core_models.CONSTANTS.DOC_ORDER_RETURN_STATUS.pending:
            return "Kutilmoqda"
        elif self.status == core_models.CONSTANTS.DOC_ORDER_RETURN_STATUS.completed:
            return "Qaytarildi"

    def calculate_return_amount(self):
        total_paid = Decimal(self.doc_purchase.paid_amount)
        total_sum = Decimal(self.doc_purchase.total_purchase_sum)
        return_amount = self.total_purchase_sum

        if total_paid < total_sum:
            remaining_balance = total_sum - total_paid
            if self.total_purchase_sum <= remaining_balance:
                return_amount = Decimal('0')
            else:
                return_amount = self.total_purchase_sum - remaining_balance
        else:
            return_amount = self.total_purchase_sum

        self.return_amount = return_amount

    def calculation(self):
        if self.status == "completed":
            if not self.returned:
                items = self.items.all()
                for i in items:
                    returned_product = DocPurchaseItem.objects.filter(
                        doc_purchase=self.doc_purchase,
                        product_id=i.product.id)
                    if returned_product.exists():
                        returned_product_first = returned_product.first()
                        instance_item = DocPurchaseReturnItem.objects.filter(pk=i.pk)
                        instance_item_quantity = instance_item.first().quantity if instance_item.first() else 0
                        returned_product_first.quantity -= instance_item_quantity
                        returned_product_first.save()

                    warehouse = Warehouse.objects.get(product_id=i.product.id)
                    warehouse.quantity -= Decimal(i.quantity)
                    warehouse.save()

                if self.doc_purchase.remaining_balance <= self.total_purchase_sum:
                    debt = core_models.OrganizationDebt.objects.last()
                    debt.debt_amount -= self.doc_purchase.remaining_balance
                    debt.save()

                    core_models.OrganizationPaymentHistory.objects.create(
                        doc_purchase=self.doc_purchase,
                        amount=self.doc_purchase.remaining_balance,
                        payment_type="payment"
                    )

                elif self.total_purchase_sum < self.doc_purchase.remaining_balance:
                    debt = core_models.OrganizationDebt.objects.last()
                    debt.debt_amount -= self.total_purchase_sum
                    debt.save()

                    core_models.OrganizationPaymentHistory.objects.create(
                        doc_purchase=self.doc_purchase,
                        amount=self.total_purchase_sum,
                        payment_type="payment"
                    )

                if self.doc_purchase.total_purchase_sum == self.doc_purchase.paid_amount:
                    self.doc_purchase.paid_amount -= self.total_purchase_sum

                self.doc_purchase.calculate_total()
                self.doc_purchase.save()

                if self.return_amount != 0:
                    self.doc_purchase.paid_amount = self.doc_purchase.total_purchase_sum
                    obj = core_models.OrganizationDebt.objects.last()
                    if obj.debt_amount == 0:
                        obj.receivable_amount = self.return_amount
                        obj.save()

                self.doc_purchase.save()

            self.returned = True

    class Meta:
        db_table = 'doc_purchase_returns'
        ordering = ["-id"]
        verbose_name = "Document Purchase Return"
        verbose_name_plural = "Document Purchase Returns"


class DocPurchaseReturnItem(core_models.BaseModel):
    doc_purchase_return = models.ForeignKey(DocPurchaseReturn, on_delete=models.CASCADE, null=True, blank=True,
                                            related_name='items')
    product = models.ForeignKey(core_models.Product, on_delete=models.SET_NULL, related_name="purchase_return",
                                null=True, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    purchase_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.pk} {self.product.name} {self.quantity}"

    def save(self, *args, **kwargs):
        self.purchase_sum = Decimal(self.quantity) * Decimal(self.purchase_price)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'doc_purchase_return_items'
        verbose_name = "Document Purchase Return Item"
        verbose_name_plural = "Document Purchase Return Items"
