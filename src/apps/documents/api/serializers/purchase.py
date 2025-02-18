from rest_framework import serializers

import src.documents.models as models


class DocPurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocPurchaseItem
        fields = ["id", "product", "quantity"]


class DocPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocPurchase
        fields = ["id", ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = f"{instance.supplier} | {instance.added_at.strftime('%d.%m.%Y %H:%M')}"
        data["debt"] = instance.remaining_balances
        return data
