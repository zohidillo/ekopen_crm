from django.db import models

from src.core.models.base import BaseModel


class Customer(BaseModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_total_debt(self):
        if self.debts.exists():
            return self.debts.first().total_debt
        else:
            return 0.00

    class Meta:
        db_table = "customers"
        ordering = ["first_name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
