from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemOptionViewSet, OrderItemViewSet, OrderItemStatusViewSet

router = DefaultRouter()
router.register(r'item_option', OrderItemOptionViewSet)
router.register(r'item', OrderItemViewSet)
router.register(r'item_status', OrderItemStatusViewSet)
router.register(r'order', OrderViewSet)  # Este siempre debe ir de último

urlpatterns = [
    path('', include(router.urls)),
]