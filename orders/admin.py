from django.contrib import admin
from .models import  Order, OrderItem, OrderItemOption, OrderItemStatus

admin.site.register(OrderItemStatus)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemOption)