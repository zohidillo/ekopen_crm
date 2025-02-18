from django.db import models
from src.core.models.base import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    order_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_category'
        ordering = ['order_num']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'


class ProductMeasurement(BaseModel):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_measurement'
        ordering = ['id']
        verbose_name = 'Product Measurement'
        verbose_name_plural = 'Product Measurements'


class Product(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,
                                 related_name="product_category", null=True, blank=True)
    measurement = models.ForeignKey(ProductMeasurement, on_delete=models.SET_NULL, null=True, blank=True)
    order_num = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.category} | {self.name} | {self.measurement.name}"

    class Meta:
        db_table = 'products'
        ordering = ['order_num']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
