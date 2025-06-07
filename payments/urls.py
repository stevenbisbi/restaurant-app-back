from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, PaymentViewSet, PaymentStatusViewSet

router = DefaultRouter()
router.register(r'', PaymentViewSet)
router.register(r'status', PaymentStatusViewSet)
router.register(r'method', PaymentMethodViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
