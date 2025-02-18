from django.db import models
import src.core.models as core_models

from decimal import Decimal
from django.utils import timezone
import src.documents.models as doc_models


class DocOrder(core_models.BaseModel):
    customer = models.ForeignKey(core_models.Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='doc_orders')
    status = models.CharField(max_length=100, choices=core_models.CONSTANTS.DOC_ORDER_STATUS.CHOICES,
                              default="pending", null=True, blank=True)
    payment_method = models.CharField(max_length=100, choices=core_models.CONSTANTS.DOC_ORDER_PAYMENT_METHOD.CHOICES,
                                      null=True, blank=True)
    payment_status = models.CharField(max_length=100, choices=core_models.CONSTANTS.DOC_ORDER_PAYMENT_STATUS.CHOICES,
                                      null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
    total_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    due_date = models.DateField(null=True, blank=True)
    waybill_path = models.CharField(max_length=500, null=True, blank=True)
    waybill_number = models.CharField(max_length=500, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.waybill_number} {self.customer.get_full_name if self.customer else None} {self.added_at.strftime('%d.%m.%Y %H:%M')}"

    @property
    def remaining_balance(self):
        return Decimal(self.total_sum) - Decimal(self.paid_amount)

    @property
    def get_status(self):
        if self.status == "pending":
            return "Kutilmoqda"
        else:
            return "Sotilgan"

    @property
    def get_payment_method(self):
        if self.payment_method == "cash":
            return "Naqt pull"
        elif self.payment_method == "card":
            return "Plastik karta"

    @property
    def get_payment_status(self):
        if self.payment_status == "paid":
            return "To'langan"
        elif self.payment_status == core_models.CONSTANTS.DOC_ORDER_PAYMENT_STATUS.partial_paid:
            return "Qisman to'langan"
        elif self.payment_status == core_models.CONSTANTS.DOC_ORDER_PAYMENT_STATUS.debt:
            return "Qarzga olingan"
        else:
            return "Muddati o'tkan"

    def check_payment_status(self):
        if timezone.now().date() > self.due_date:
            self.payment_status = "overdue"
            self.save()

    def save(self, *args, **kwargs):
        if self.paid_amount == 0:
            self.payment_status = "debt"
        elif self.paid_amount == self.total_sum:
            self.payment_status = "paid"
        elif 0 < self.paid_amount < self.total_sum:
            self.payment_status = "partial_paid"
        if not self.waybill_number:
            last_order = DocOrder.objects.all().order_by('id').last()
            if last_order:
                last_number = int(last_order.waybill_number.split('-')[-1])
                self.waybill_number = f'YX-{last_number + 1:04d}'
            else:
                self.waybill_number = 'YX-0001'
        self.calculation()
        super().save(*args, **kwargs)

    def calculate_total_sum(self):
        items = self.items.all()
        total_sum = 0
        for item in items:
            total_sum += item.sale_sum
        self.total_sum = total_sum
        self.save()

    def calculation(self):
        if self.status == core_models.CONSTANTS.DOC_ORDER_STATUS.completed:
            if not self.is_completed:
                doc = self
                items = doc.items.all()
                for item in items:
                    warehouse = doc_models.Warehouse.objects.get(pk=item.product.id)
                    warehouse.quantity -= item.quantity
                    warehouse.save()

                # calculate payments
                debt = doc.total_sum - doc.paid_amount
                core_models.PaymentHistory.objects.create(
                    doc_order=doc,
                    customer=doc.customer,
                    amount=doc.paid_amount,
                    payment_type="payment"
                )
                if debt > 0:
                    debts = core_models.CustomerDebt.objects.filter(customer=doc.customer)
                    core_models.PaymentHistory.objects.create(
                        doc_order=doc,
                        customer=doc.customer,
                        amount=Decimal(debt),
                        payment_type="debt"
                    )
                    if debts.exists():
                        first_debt = debts.first()
                        first_debt.total_debt += Decimal(debt)
                        first_debt.save()
                    else:
                        core_models.CustomerDebt.objects.create(customer=doc.customer, total_debt=Decimal(debt))
                self.is_completed = True
                self.save()

    @property
    def get_all_total_quantity(self):
        return sum([i.quantity for i in self.items.all()])

    class Meta:
        db_table = 'doc_orders'
        ordering = ['-id']
        verbose_name = 'Document Order'
        verbose_name_plural = 'Document Orders'


class DocOrderItem(core_models.BaseModel):
    doc_order = models.ForeignKey(DocOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    category = models.ForeignKey(core_models.ProductCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='doc_order_items')
    product = models.ForeignKey("Warehouse", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='doc_order_items')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sale_sum = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.id} {self.doc_order} item"

    def save(self, *args, **kwargs):
        self.category = self.product.product.category
        self.sale_price = self.product.sell_price
        self.sale_sum = self.quantity * self.sale_price
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'doc_order_items'
        verbose_name = 'Document Order Item'
        verbose_name_plural = 'Document Order Items'
