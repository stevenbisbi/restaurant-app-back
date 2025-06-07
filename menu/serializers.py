from rest_framework import serializers
from .models import Menu, MenuItem, MenuItemVariant, MenuItemOption
from restaurant.serializers import RestaurantSerializer
from restaurant.models import Restaurant

class MenuSerializer(serializers.ModelSerializer):
    # Campo para escritura: acepta el UUID del restaurante
    restaurant = serializers.SlugRelatedField(
        slug_field='id',  # Usa el UUID como identificador
        queryset=Restaurant.objects.all()  # Valida que exista el restaurante
    )
    
    # Campo para lectura: muestra los detalles del restaurante
    restaurant_details = RestaurantSerializer(source='restaurant', read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        extra_fields = ['restaurant_details']  # Campo adicional para la respuesta

class MenuItemOptionSerializer(serializers.ModelSerializer):
  class Meta:
    model = MenuItemOption
    fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
  options = MenuItemOptionSerializer(many=True, read_only=True)
  class Meta:
    model = MenuItem
    fields = [
            'id', 'category', 'name', 'description', 'price', 'image',
            'is_vegetarian', 'is_featured', 'is_promotion', 'is_available',
            'created_at', 'updated_at', 'options'
        ]

class MenuItemVariantSerializer(serializers.ModelSerializer):
  class Meta:
    model = MenuItemVariant
    fields = '__all__'

