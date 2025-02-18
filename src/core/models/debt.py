from django.db import models

import src.core.models.base as core_models
import src.core.models.contants as constants


class CustomerDebt(core_models.BaseModel):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name='debts')
    total_debt = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer.get_full_name} - {self.total_debt}"

    class Meta:
        db_table = 'customer_debts'
        app_label = 'core'
        verbose_name = 'Customer Debt'
        verbose_name_plural = 'Customer Debts'


class PaymentHistory(core_models.BaseModel):
    doc_order = models.ForeignKey("documents.DocOrder", on_delete=models.SET_NULL,
                                  related_name='payments', null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name='payment_history')
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=20, choices=constants.CONSTANTS.PAYMENT_TYPE.CHOICES,
                                    null=True, blank=True)
    old_debt = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.customer.get_full_name} {self.amount}"

    class Meta:
        db_table = 'payment_history'
        ordering = ('-id',)
        app_label = 'core'
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payment History'


class OrganizationDebt(core_models.BaseModel):
    debt_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    receivable_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.debt_amount} {self.updated_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        db_table = 'organization_debts'
        ordering = ('-id',)
        app_label = 'core'
        verbose_name = 'Organization Debt'
        verbose_name_plural = 'Organization Debts'


class OrganizationPaymentHistory(core_models.BaseModel):
    doc_purchase = models.ForeignKey("documents.DocPurchase", on_delete=models.CASCADE,
                                     related_name='organization_payment_history', null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=20, choices=constants.CONSTANTS.PAYMENT_TYPE.CHOICES,
                                    null=True, blank=True)

    def __str__(self):
        return f"{self.amount} {self.payment_type} {self.added_at.strftime('%d.%m.%Y %H:%M')}"

    class Meta:
        db_table = 'organization_payment_history'
        ordering = ('-id',)
        app_label = 'core'
        verbose_name = 'Organization Payment History'
        verbose_name_plural = 'Organization Payment History'
