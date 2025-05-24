from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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
    anio = models.IntegerField()
    tipo = models.CharField(max_length=11, choices=TIPOS)
    numero_serie = models.CharField(max_length=50)
    kilometraje_actual = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultimo_mantenimiento = models.DateField()
    estado = models.CharField(max_length=17, choices=ESTADOS, default='activo')
    observaciones = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

    def actualizar_estado(self):
        # 1. Verificar si tiene ALGÚN mantenimiento correctivo (sin importar estado)
        if self.mantenimientocorrectivo_set.exists():
            self.estado = 'inactivo'
        # 2. Si no tiene correctivos, verificar si tiene mantenimientos en proceso
        elif (self.mantenimientopreventivo_set.filter(estado='en_proceso').exists() or 
              self.mantenimientocorrectivo_set.filter(estado='en_proceso').exists()):
            self.estado = 'en_mantenimiento'
        # 3. Si no cumple las anteriores, verificar si no hay pendientes
        else:
            # Verificar preventivos pendientes (diferentes de completado/cancelado)
            preventivos_pendientes = self.mantenimientopreventivo_set.exclude(
                estado__in=['completado', 'cancelado']
            ).exists()
            
            # Verificar correctivos pendientes (diferentes de completado/cancelado)
            correctivos_pendientes = self.mantenimientocorrectivo_set.exclude(
                estado__in=['completado', 'cancelado']
            ).exists()
            
            if not preventivos_pendientes and not correctivos_pendientes:
                self.estado = 'activo'
        
        self.save()


class MantenimientoPreventivo(models.Model):
    ESTADOS = (
        ('reportado', 'Reportado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    km_prox_mantenimiento = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_prox_mantenimiento = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    repuestos_utilizados = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Preventivo {self.id} - {self.vehiculo.placa}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vehiculo.actualizar_estado()


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
    solucion_aplicada = models.TextField()
    repuestos_utilizados = models.TextField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='reportado')
    prioridad = models.CharField(max_length=5, choices=PRIORIDADES, default='media')
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_solucion = models.DateField()
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Correctivo {self.id} - {self.vehiculo.placa}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vehiculo.actualizar_estado()


# Señales para actualizar estado al eliminar mantenimientos
@receiver(post_delete, sender=MantenimientoPreventivo)
def actualizar_al_eliminar_preventivo(sender, instance, **kwargs):
    instance.vehiculo.actualizar_estado()

@receiver(post_delete, sender=MantenimientoCorrectivo)
def actualizar_al_eliminar_correctivo(sender, instance, **kwargs):
    instance.vehiculo.actualizar_estado()