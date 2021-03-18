from rest_framework import viewsets, permissions
from ..serializers import ServiceSerializer
from ...models import Service


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('name')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
