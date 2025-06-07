from rest_framework import viewsets
from .models import Order, OrderItem, OrderItemOption, OrderItemStatus
from .serializers import OrderSerializer,OrderItemOptionSerializer, OrderItemSerializer, OrderItemStatusSerializer

class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer

class OrderItemOptionViewSet(viewsets.ModelViewSet):
  queryset = OrderItemOption.objects.all()
  serializer_class = OrderItemOptionSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
  queryset = OrderItem.objects.all()
  serializer_class = OrderItemSerializer

class OrderItemStatusViewSet(viewsets.ModelViewSet):
  queryset = OrderItemStatus.objects.all()
  serializer_class = OrderItemStatusSerializer
