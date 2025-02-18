from rest_framework import serializers

import src.core.models as models


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ("id", "get_full_name", "get_total_debt", "phone_number")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = f"{instance.get_full_name} | {instance.get_total_debt}"
        return data


class CustomerDebtPaymentSerializer(serializers.Serializer):
    customer = serializers.IntegerField()
    debt = serializers.DecimalField(max_digits=16, decimal_places=2)
