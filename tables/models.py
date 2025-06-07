from django.db import models
import uuid
from restaurant.models import Restaurant
# Create your models here.

class Table(models.Model):
    STATUS_CHOICES= [
        ('Available', 'Disponible'),
        ('Occupied', 'Ocupada'),
        ('Reserved', 'Reservada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="tables")
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    location = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # Could be 'Available', 'Occupied', 'Reserved'
    qr_code_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.number}"

