from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('tecnico', 'Técnico'),
    )
    rol = models.CharField(max_length=13, choices=ROLES, default='tecnico')
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class Vehiculo(models.Model):
    TIPOS = (
        ('camion', 'Camión'),
        ('furgoneta', 'Furgoneta'),
        ('automovil', 'Automóvil'),
        ('motocicleta', 'Motocicleta'),
        ('otro', 'Otro'),
    )
    ESTADOS = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('en_mantenimiento', 'En Mantenimiento'),
        ('desincorporado', 'Desincorporado'),
    )
    
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=11, choices=TIPOS)
    numero_serie = models.CharField(max_length=50, null=True, blank=True)
    kilometraje_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_ultimo_mantenimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=17, choices=ESTADOS, default='activo')
    observaciones = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

class MantenimientoPreventivo(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    km_prox_mantenimiento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_prox_mantenimiento = models.DateField(null=True, blank=True)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    repuestos_utilizados = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Preventivo {self.id} - {self.vehiculo.placa}"

class MantenimientoCorrectivo(models.Model):
    ESTADOS = (
        ('reportado', 'Reportado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    PRIORIDADES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    )
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    descripcion_falla = models.TextField()
    solucion_aplicada = models.TextField(null=True, blank=True)
    repuestos_utilizados = models.TextField(null=True, blank=True)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='reportado')
    prioridad = models.CharField(max_length=5, choices=PRIORIDADES, default='media')
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_solucion = models.DateField(null=True, blank=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Correctivo {self.id} - {self.vehiculo.placa}"