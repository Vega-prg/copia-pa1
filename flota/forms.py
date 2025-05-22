from django import forms
from .models import Vehiculo, MantenimientoPreventivo, MantenimientoCorrectivo
from django.utils import timezone
from django.core.exceptions import ValidationError
import re

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['usuario_registro', 'fecha_registro']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ABC123',
                'pattern': '^[A-Z0-9]{6}$',
                'title': 'La placa debe contener exactamente 6 caracteres alfanuméricos (letras y números sin guiones)'
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
                'placeholder': 'Ej: 2020',
                'min': '1900',
                'max': timezone.now().year,
                'required': True
            }),
            'numero_serie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1HGCM82633A004352',
                'pattern': '^.{17}$',
                'title': 'Debe contener exactamente 17 caracteres'
            }),
            'kilometraje_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'min': '0',
                'placeholder': 'Ej: 50000'
            }),
            'fecha_ultimo_mantenimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'max': timezone.now().date()
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
                'placeholder': 'Detalles adicionales (opcional)'
            }),
        }
        labels = {
            'placa': 'Placa del vehículo',
            'anio': 'Año',
            'numero_serie': 'Número de serie',
            'kilometraje_actual': 'Kilometraje actual (km)',
            'fecha_ultimo_mantenimiento': 'Fecha último mantenimiento',
        }

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        if not re.match(r'^[A-Z0-9]{6}$', placa):
            raise ValidationError('La placa debe tener exactamente 6 caracteres alfanuméricos, sin guiones ni espacios.')
        return placa.upper()

    def clean_kilometraje_actual(self):
        km = self.cleaned_data.get('kilometraje_actual')
        if km is not None and km < 0:
            raise ValidationError('El kilometraje no puede ser negativo.')
        return km

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        año_actual = timezone.now().year
        if anio > año_actual:
            raise ValidationError('El año no puede ser mayor al actual.')
        if anio < 1900:
            raise ValidationError('El año debe ser mayor a 1900.')
        return anio

    def clean_fecha_ultimo_mantenimiento(self):
        fecha = self.cleaned_data.get('fecha_ultimo_mantenimiento')
        if fecha > timezone.now().date():
            raise ValidationError('La fecha no puede ser mayor que hoy.')
        return fecha

    def clean_numero_serie(self):
        serie = self.cleaned_data.get('numero_serie')
        if not serie or len(serie) != 17:
            raise ValidationError('El número de serie debe tener exactamente 17 caracteres.')
        return serie.upper()

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
            'repuestos_utilizados': 'Repuestos/materiales utilizados',
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
