from rest_framework import serializers
from .models import Reservation, ReservationStatus

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationStatus
        fields = ['id', 'name', 'description']


#toca crear un status, quede en como esta el Chatgpt