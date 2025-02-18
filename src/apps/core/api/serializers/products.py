from rest_framework import serializers

import src.core.models as models
import src.documents.models as document_models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ["id", "name"]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = models.Product
        fields = ("id", "name", "category")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, "party_item_quantity"):
            data["party_item_quantity"] = instance.party_item_quantity
        return data


class WarehouseListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = document_models.Warehouse
        fields = ("id", "product", "quantity")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = f"{instance.product.category} | {instance.product.name} | {instance.product.measurement}"
        if hasattr(instance, "order_item_quantity"):
            data["order_item_quantity"] = instance.order_item_quantity
        return data
