from decimal import Decimal

from django.db import models
import src.core.models as core_models


class Warehouse(core_models.BaseModel):
    category = models.ForeignKey(core_models.ProductCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='warehouse')
    product = models.ForeignKey(core_models.Product, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='warehouse')
    quantity = models.PositiveIntegerField(null=True, blank=True)
    sell_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.product.name} {self.quantity}'

    def save(self, *args, **kwargs):
        self.category = self.product.category
        super().save(*args, **kwargs)

    @property
    def get_total_sell_price(self):
        return Decimal(self.quantity) * Decimal(self.sell_price)

    class Meta:
        db_table = 'warehouse'
        ordering = ['-added_at']
        verbose_name = 'Warehouse'
        app_label = 'documents'
        verbose_name_plural = 'Warehouses'


class ProductResidual(models.Model):
    party = models.ForeignKey("DocPurchase", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(core_models.Product, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='residuals')
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.product.name} {self.quantity}'

    class Meta:
        db_table = 'product_residuals'
        verbose_name = 'Product Residual'
        verbose_name_plural = 'Product Residuals'
