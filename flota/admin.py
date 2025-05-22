from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Vehiculo, MantenimientoPreventivo, MantenimientoCorrectivo

# Configuración para Usuario (se mantiene igual)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Datos Adicionales', {
            'fields': ('rol', 'activo', 'ultimo_login'),
        }),
    )

# Configuración para Vehículos (se mantiene igual)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'tipo', 'estado', 'kilometraje_actual', 'usuario_registro')
    list_filter = ('tipo', 'estado', 'marca')
    search_fields = ('placa', 'marca', 'modelo', 'numero_serie')
    raw_id_fields = ('usuario_registro',)
    date_hierarchy = 'fecha_registro'

# Configuración BASE para Mantenimientos (MODIFICADA)
class MantenimientoBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estado', 'usuario_registro')
    list_filter = ('estado',)
    raw_id_fields = ('vehiculo', 'usuario_registro')

# Configuración para MantenimientoPreventivo (MODIFICADA)
class MantenimientoPreventivoAdmin(MantenimientoBaseAdmin):
    list_display = MantenimientoBaseAdmin.list_display + ('tipo', 'fecha_prox_mantenimiento')
    date_hierarchy = 'fecha_registro'  # Este sí existe en Preventivo
    
    fieldsets = (
        (None, {
            'fields': ('vehiculo', 'tipo', 'descripcion', 'usuario_registro')
        }),
        ('Programación', {
            'fields': ('km_prox_mantenimiento', 'fecha_prox_mantenimiento')
        }),
        ('Detalles', {
            'fields': ('presupuesto', 'repuestos_utilizados', 'estado')
        }),
    )

# Configuración para MantenimientoCorrectivo (MODIFICADA)
class MantenimientoCorrectivoAdmin(MantenimientoBaseAdmin):
    list_display = MantenimientoBaseAdmin.list_display + ('prioridad', 'fecha_reporte', 'fecha_solucion')
    list_filter = MantenimientoBaseAdmin.list_filter + ('prioridad',)
    date_hierarchy = 'fecha_reporte'  # Usamos el campo correcto
    
    fieldsets = (
        (None, {
            'fields': ('vehiculo', 'prioridad', 'descripcion_falla', 'usuario_registro')
        }),
        ('Solución', {
            'fields': ('solucion_aplicada', 'fecha_solucion')
        }),
        ('Detalles', {
            'fields': ('presupuesto', 'repuestos_utilizados', 'estado')
        }),
    )

# Registro final
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(MantenimientoPreventivo, MantenimientoPreventivoAdmin)
admin.site.register(MantenimientoCorrectivo, MantenimientoCorrectivoAdmin)