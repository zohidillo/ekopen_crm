from decimal import Decimal
from django.db import models
import src.core.models as core_models


class DocPurchase(core_models.BaseModel):
    supplier = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=core_models.CONSTANTS.DOC_PURCHASE_STATUS.CHOICES,
                              default="pending", null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    total_purchase_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    writen_to_warehouse = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.supplier} {self.added_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def remaining_balance(self):
        return Decimal(self.total_purchase_sum) - Decimal(self.paid_amount)

    @property
    def get_status(self):
        if self.status == "pending":
            return "Kutilyapti"
        else:
            return "Sotib olingan"

    def calculate_total(self):
        items = self.items.all()
        total = 0
        for i in items:
            total += i.purchase_sum
        self.total_purchase_sum = total

    def calculation(self):
        import src.documents.models as document_models

        if self.status == "completed":
            if not self.writen_to_warehouse:
                items = self.items.all()
                for i in items:
                    document_models.ProductResidual.objects.create(
                        product_id=i.product.id,
                        quantity=i.quantity,
                        party=self
                    )
                if self.paid_amount != 0:
                    core_models.OrganizationPaymentHistory.objects.create(
                        doc_purchase=self,
                        amount=self.paid_amount,
                        payment_type=core_models.constants.CONSTANTS.PAYMENT_TYPE.payment
                    )
                if self.paid_amount == self.total_purchase_sum:
                    ...
                elif self.paid_amount < self.total_purchase_sum:
                    debts = core_models.OrganizationDebt.objects.all()
                    if debts.exists():
                        debt = debts.first()
                        debt.debt_amount += self.remaining_balance
                        debt.save()
                    else:
                        debts.create(debt_amount=self.remaining_balance)
                    core_models.OrganizationPaymentHistory.objects.create(
                        doc_purchase=self,
                        amount=self.remaining_balance,
                        payment_type=core_models.constants.CONSTANTS.PAYMENT_TYPE.debt
                    )
            self.writen_to_warehouse = True

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
            self.calculate_total()
        else:
            self.calculate_total()
            self.calculation()
            super().save(*args, **kwargs)

    class Meta:
        db_table = 'doc_purchases'
        ordering = ["-id"]
        verbose_name = 'DocPurchase'
        verbose_name_plural = 'DocPurchases'


class DocPurchaseItem(core_models.BaseModel):
    doc_purchase = models.ForeignKey(DocPurchase, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='items')
    category = models.ForeignKey(core_models.ProductCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='doc_purchase_item')
    product = models.ForeignKey(core_models.Product, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='doc_purchase_item')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    purchase_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def save(self, *args, **kwargs):
        self.category = self.product.category
        self.purchase_sum = self.quantity * self.purchase_price
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'doc_purchase_items'
        ordering = ["-id", "doc_purchase"]
        verbose_name = 'DocPurchase Item'
        verbose_name_plural = 'DocPurchase Items'
