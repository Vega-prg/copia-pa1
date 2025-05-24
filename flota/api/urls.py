from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, MantenimientoPreventivoViewSet  # Importa desde el mismo paquete

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'mantenimientos-preventivos', MantenimientoPreventivoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]