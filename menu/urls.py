from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, MenuItemViewSet, MenuItemVariantViewSet, MenuItemOptionViewSet, get_category_choices

router = DefaultRouter()
router.register(r'menus', MenuViewSet)
router.register(r'items', MenuItemViewSet)
router.register(r'item_variants', MenuItemVariantViewSet)
router.register(r'item_option', MenuItemOptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', get_category_choices),
]
