from django.dispatch import receiver
from django.db.models.signals import post_save

import src.core.models as models


@receiver(post_save, sender=models.Customer)
def create_debt(sender, instance, created, **kwargs):
    if created:
        models.CustomerDebt.objects.create(
            created_by=instance.created_by,
            customer=instance, total_debt=0.00
        )
