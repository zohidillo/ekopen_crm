from django.dispatch import receiver
from django.db.models.signals import post_save

import src.documents.models as models


@receiver(post_save, sender=models.ProductResidual)
def write_to_warehouse(sender, instance, **kwargs):
    warehouse = models.Warehouse.objects.filter(product=instance.product)
    if warehouse.exists():
        warehouse_first = warehouse.first()
        total_quantity = models.ProductResidual.objects.filter(product=instance.product).order_by("-id").first()
        warehouse_first.quantity += total_quantity.quantity
        warehouse_first.save()
    else:
        models.Warehouse.objects.create(product=instance.product, quantity=instance.quantity)
