from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

import src.documents.models as models
import src.apps.documents.api.serializers as serializers


class DetailDocOrderAPIView(RetrieveAPIView, GenericViewSet):
    queryset = models.DocOrder.objects.select_related("customer", "created_by", "modified_by")
    serializer_class = serializers.GetDocOrderSerializer
    permission_classes = [IsAuthenticated]
