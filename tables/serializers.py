from rest_framework import serializers
from .models import Table
from reservations.models import Reservation  # si tienes un modelo separado

class TableSerializer(serializers.ModelSerializer):
  is_reserved = serializers.SerializerMethodField()

  class Meta:
    model = Table
    fields = '__all__'  # o explícitamente incluye los campos

  def get_is_reserved(self, obj):
    return obj.reservations.filter(status__name='active').exists()
