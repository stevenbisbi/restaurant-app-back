from django.contrib import admin
from .models import PaymentMethod,PaymentStatus, Payment

admin.site.register(PaymentMethod)
admin.site.register(PaymentStatus)
admin.site.register(Payment)
