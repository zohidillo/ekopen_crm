from rest_framework import serializers

import src.documents.models as models
import src.core.models as core_models
from src.apps.documents.api.serializers.base import build_relational_model_serializer as base_ser


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocOrder
        fields = ("id", "customer", "total_sum")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = f"{instance.waybill_number} | {instance.added_at.strftime('%d.%m.%Y %H:%M')}"
        if hasattr(instance, "remaining_balances"):
            data["remaining_balances"] = instance.remaining_balances
        return data


class WarehouseSerializer(serializers.ModelSerializer):
    product = base_ser(core_models.Product, fields_=("id", "name"))

    class Meta:
        model = models.Warehouse
        fields = ("id", "product")


class DocOrderItemsSerializer(serializers.ModelSerializer):
    product = WarehouseSerializer()
    category = base_ser(core_models.ProductCategory, fields_=("id", "name"))

    class Meta:
        model = models.DocOrderItem
        exclude = ("doc_order", "added_at", "updated_at", "created_by", "modified_by")


class PostDocOrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=base_ser(models.DocOrderItem, fields_=("product", "quantity")), required=True)

    class Meta:
        model = models.DocOrder
        exclude = (
            "is_completed", "waybill_path", "added_at",
            "total_sum", "waybill_number", "updated_at", "created_by", "modified_by"
        )


class GetDocOrderSerializer(serializers.ModelSerializer):
    items = DocOrderItemsSerializer(many=True)
    customer = base_ser(core_models.Customer, fields_=("id", "first_name", "last_name", "phone_number"))

    class Meta:
        model = models.DocOrder
        exclude = ("is_completed", "waybill_path", "added_at", "updated_at", "created_by", "modified_by")
