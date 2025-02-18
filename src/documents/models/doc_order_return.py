from decimal import Decimal

from django.db import models

import src.core.models as core_models
import src.documents.models as document_models


class DocOrderReturn(core_models.BaseModel):
    doc_order = models.ForeignKey("DocOrder", on_delete=models.CASCADE, related_name="return_order", null=True,
                                  blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True,
                              choices=core_models.CONSTANTS.DOC_ORDER_RETURN_STATUS.CHOICES, default="pending")
    total_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    return_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doc_order} - {self.reason}"

    @property
    def get_status(self):
        if self.status == "pending":
            return "Kutilmoqda"
        else:
            return "Qaytarib olindi"

    def calculate_return_amount(self):
        total_paid = Decimal(self.doc_order.paid_amount)
        total_sum = Decimal(self.doc_order.total_sum)
        return_amount = self.total_sum

        if total_paid < total_sum:
            remaining_balance = total_sum - total_paid
            if self.total_sum <= remaining_balance:
                return_amount = Decimal('0')
            else:
                return_amount = self.total_sum - remaining_balance
        else:
            return_amount = self.total_sum

        self.return_amount = return_amount

    def fix_amounts(self):
        if self.status == "completed":
            if not self.returned:
                items = self.items.all()
                for item in items:
                    order_item = document_models.DocOrderItem.objects.filter(doc_order=self.doc_order,
                                                                             product=item.product)
                    order_item_first = order_item.first()
                    order_item_first.quantity -= item.quantity
                    order_item_first.save()

                    warehouse = document_models.Warehouse.objects.get(pk=item.product.pk)
                    warehouse.quantity += item.quantity
                    warehouse.save()

                if self.doc_order.remaining_balance <= self.total_sum:
                    debt = core_models.CustomerDebt.objects.filter(customer=self.doc_order.customer)
                    first_debt = debt.first()
                    first_debt.total_debt -= self.doc_order.remaining_balance
                    first_debt.save()

                    core_models.PaymentHistory.objects.create(
                        doc_order=self.doc_order,
                        customer=self.doc_order.customer,
                        amount=self.doc_order.remaining_balance,
                        payment_type="payment"
                    )

                elif self.total_sum < self.doc_order.remaining_balance:
                    debt = core_models.CustomerDebt.objects.filter(customer=self.doc_order.customer)
                    first_debt = debt.first()
                    first_debt.total_debt -= self.total_sum
                    first_debt.save()

                    core_models.PaymentHistory.objects.create(
                        doc_order=self.doc_order,
                        customer=self.doc_order.customer,
                        amount=self.total_sum,
                        payment_type="payment"
                    )

                if self.doc_order.total_sum == self.doc_order.paid_amount:
                    self.doc_order.paid_amount -= self.total_sum

                self.doc_order.calculate_total_sum()

                if self.return_amount != 0:
                    self.doc_order.paid_amount = self.doc_order.total_sum

                self.doc_order.save()
                self.returned = True

    class Meta:
        db_table = "doc_order_returns"
        ordering = ["-id"]
        verbose_name = "Document Order Return"
        verbose_name_plural = "Document Order Returns"


class DocOrderReturnItem(core_models.BaseModel):
    return_order = models.ForeignKey("DocOrderReturn", on_delete=models.CASCADE,
                                     related_name="items", null=True, blank=True)
    product = models.ForeignKey("Warehouse", on_delete=models.CASCADE,
                                related_name="return_order", null=True, blank=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sold_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sold_price_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.return_order} - {self.product} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.sold_price = self.product.sell_price
        self.sold_price_sum = self.quantity * self.sold_price
        super().save(*args, **kwargs)

    class Meta:
        db_table = "doc_order_returns_items"
        ordering = ["-id"]
        verbose_name = "Document Order Return Item"
        verbose_name_plural = "Document Order Return Items"
