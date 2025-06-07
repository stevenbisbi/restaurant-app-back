from rest_framework import serializers
from .models import Order, OrderItem, OrderItemOption, OrderItemStatus



class OrderItemOptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItemOption
    fields = '__all__'
    
class OrderItemSerializer(serializers.ModelSerializer):
  options = OrderItemOptionSerializer(many=True, read_only=True)
  status = serializers.StringRelatedField()  # Muestra el nombre del estado
  class Meta:
    model = OrderItem
    fields = '__all__'

      
class OrderItemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemStatus
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Order
    fields = '__all__'