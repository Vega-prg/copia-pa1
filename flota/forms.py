from django import forms
from .models import Vehiculo, MantenimientoPreventivo, MantenimientoCorrectivo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['usuario_registro', 'fecha_registro']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ABC-123'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Toyota'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Corolla'
            }),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2020'
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opcional'
            }),
            'kilometraje_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'fecha_ultimo_mantenimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalles adicionales...'
            }),
        }
        labels = {
            'placa': 'Placa del vehículo',
            'anio': 'Año',
            'numero_serie': 'Número de serie',
            'kilometraje_actual': 'Kilometraje actual (km)',
            'fecha_ultimo_mantenimiento': 'Fecha último mantenimiento',
        }

class MantenimientoPreventivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoPreventivo
        exclude = ['usuario_registro', 'fecha_registro']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione un vehículo'
            }),
            'tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cambio de aceite'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa el mantenimiento...'
            }),
            'km_prox_mantenimiento': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 10000',
                'step': '0.01'
            }),
            'fecha_prox_mantenimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'presupuesto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 150.00',
                'step': '0.01'
            }),
            'repuestos_utilizados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Lista de repuestos...'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'km_prox_mantenimiento': 'Próximo mantenimiento (km)',
            'fecha_prox_mantenimiento': 'Fecha próximo mantenimiento',
            'repuestos_utilizados': 'Repuestos/materials utilizados',
        }

class MantenimientoCorrectivoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoCorrectivo
        exclude = ['usuario_registro', 'fecha_reporte']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Seleccione un vehículo'
            }),
            'descripcion_falla': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa la falla...'
            }),
            'solucion_aplicada': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa la solución aplicada...'
            }),
            'repuestos_utilizados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Lista de repuestos...'
            }),
            'presupuesto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 250.00',
                'step': '0.01'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_solucion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'descripcion_falla': 'Descripción de la falla',
            'solucion_aplicada': 'Solución aplicada',
            'repuestos_utilizados': 'Repuestos utilizados',
            'fecha_solucion': 'Fecha de solución',
        }