from rest_framework import serializers


def build_relational_model_serializer(model_, fields_=None, exclude_=None, ref_name_=None):
    class RelationalSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_
            if fields_ is not None:
                fields = fields_
            else:
                exclude = exclude_
            ref_name = ref_name_

    return RelationalSerializer()
