from django.contrib import admin
from .models import ReservationStatus, Reservation

admin.site.register(ReservationStatus)
admin.site.register(Reservation)
