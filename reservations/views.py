from rest_framework import viewsets
from rest_framework.response import Response
from .models import Reservation, ReservationStatus
from .serializers import ReservationSerializer, ReservationStatusSerializer
from tables.models import Table

class ReservationViewSet(viewsets.ModelViewSet):
  queryset = Reservation.objects.all()
  serializer_class = ReservationSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    reservation = Reservation.objects.get(id=response.data['id'])
    return Response({
      **response.data,
      'table': {
          'id': reservation.table.id,
          'is_reserved': True,
          'status': 'Reserved',
          # Puedes agregar más campos del table si los necesitas
          'number': reservation.table.number,
          'capacity': reservation.table.capacity,
          # etc.
      }
  })

  def perform_create(self, serializer):
    reservation = serializer.save()
    table = reservation.table
    table.is_reserved = True
    table.status = "Reserved"
    table.save()

  def perform_destroy(self, instance):
    table = instance.table
    table.is_reserved = False
    table.status = "Available"
    table.save()
    instance.delete()

  def perform_update(self, serializer):
    reservation = serializer.save()
    table = reservation.table
    if reservation.status.name.lower() in ["cancelled", "completed"]:
      table.is_reserved = False
      table.status = "Available"
      table.save()

class ReservationStatusViewSet(viewsets.ModelViewSet):
  queryset = ReservationStatus.objects.all()
  serializer_class = ReservationStatusSerializer