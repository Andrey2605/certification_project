from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from market.models import Consumer, Product, Supplier
from market.serializers import (ConsumerSerializer, ProductSerializer,
                                SupplierSerializer)
from users.permissions import IsActiveUser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]
    permission_classes = [IsActiveUser]


class ConsumerViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]
    permission_classes = [IsActiveUser]
