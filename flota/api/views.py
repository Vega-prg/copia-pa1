from rest_framework import viewsets
from ..models import Vehiculo, MantenimientoPreventivo  # Importa desde la raíz de la app
from ..serializers import VehiculoSerializer, MantenimientoPreventivoSerializer  # Asume que crearás este archivo

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class MantenimientoPreventivoViewSet(viewsets.ModelViewSet):
    queryset = MantenimientoPreventivo.objects.all()
    serializer_class = MantenimientoPreventivoSerializer