from rest_framework import serializers
from .models import Vehiculo, Usuario, MantenimientoPreventivo

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'  # O selecciona campos específicos: ['placa', 'marca', ...]

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'rol']

class MantenimientoPreventivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MantenimientoPreventivo
        fields = '__all__'