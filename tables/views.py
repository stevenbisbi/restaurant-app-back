from rest_framework import viewsets
from .models import Table
from .serializers import TableSerializer

class TableViewSet(viewsets.ModelViewSet):
  queryset = Table.objects.all()
  serializer_class = TableSerializer

  def get_queryset(self):
    # Asegurarse de que siempre devuelva los campos necesarios
    return Table.objects.all().select_related('restaurant')