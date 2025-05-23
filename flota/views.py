from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehiculo, MantenimientoPreventivo, MantenimientoCorrectivo
from .forms import VehiculoForm, MantenimientoPreventivoForm, MantenimientoCorrectivoForm
from datetime import date, timedelta  # Importaciones añadidas para manejo de fechas
from django.utils import timezone
from itertools import chain
from django.db.models import F, Value
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from .decorators import rol_requerido


def error_403(request, exception):
    return render(request, '403.html', status=403)


@login_required
def dashboard(request):
    # Totales
    total_vehiculos = Vehiculo.objects.count()
    vehiculos_en_taller = Vehiculo.objects.filter(estado='en_mantenimiento').count()
    
    # Mantenimientos
    preventivos_pendientes = MantenimientoPreventivo.objects.filter(estado='pendiente')
    correctivos_activos = MantenimientoCorrectivo.objects.exclude(estado__in=['completado', 'cancelado'])
    
    # Próximos mantenimientos (7 días)
    fecha_limite = timezone.now() + timedelta(days=7)
    proximos_mantenimientos = MantenimientoPreventivo.objects.filter(
        fecha_prox_mantenimiento__lte=fecha_limite,
        estado='pendiente'
    ).order_by('fecha_prox_mantenimiento')[:5]
    
    # Correctivos recientes
    correctivos_recientes = MantenimientoCorrectivo.objects.order_by('-fecha_reporte')[:5]
    
    # Alertas recientes
    alertas_recientes = []
    hoy = date.today()
    for mp in MantenimientoPreventivo.objects.filter(estado='pendiente'):
        if mp.fecha_prox_mantenimiento and (mp.fecha_prox_mantenimiento - hoy) <= timedelta(days=3):
            alertas_recientes.append({
                'titulo': f'Mantenimiento Preventivo: {mp.tipo}',
                'descripcion': f'Vence el {mp.fecha_prox_mantenimiento.strftime("%d/%m/%Y")}',
                'fecha': mp.fecha_prox_mantenimiento,
                'vehiculo': mp.vehiculo
            })
    
    return render(request, 'flota/dashboard.html', {
        'total_vehiculos': total_vehiculos,
        'vehiculos_en_taller': vehiculos_en_taller,
        'preventivos_pendientes': preventivos_pendientes,
        'correctivos_activos': correctivos_activos,
        'proximos_mantenimientos': proximos_mantenimientos,
        'correctivos_recientes': correctivos_recientes,
        'alertas_recientes': alertas_recientes[:3]  # Mostrar solo 3 alertas
    })

@login_required
@rol_requerido('administrador') 
def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario_registro = request.user
            vehiculo.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('lista_vehiculos')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = VehiculoForm(instance=vehiculo)
    
    return render(request, 'flota/vehiculos/editar.html', {'form': form, 'vehiculo': vehiculo})

@login_required
def detalle_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    # Obtener mantenimientos relacionados
    mantenimientos_preventivos = MantenimientoPreventivo.objects.filter(vehiculo=vehiculo)
    mantenimientos_correctivos = MantenimientoCorrectivo.objects.filter(vehiculo=vehiculo)
    return render(request, 'flota/vehiculos/detalle.html', {
        'vehiculo': vehiculo,
        'preventivos': mantenimientos_preventivos,
        'correctivos': mantenimientos_correctivos
    })

ESTADOS = {
    'activo': 'Activo',
    'inactivo': 'Inactivo',
    'en_mantenimiento': 'En mantenimiento',
    'desincorporado': 'Desincorporado',
}

BADGE_CLASSES = {
    'activo': 'bg-success',
    'en_mantenimiento': 'bg-warning text-dark',
    'desincorporado': 'bg-secondary',
    'fuera_servicio': 'bg-danger'
}

@login_required
def lista_vehiculos(request):
    estado = request.GET.get('estado')
    vehiculos_qs = Vehiculo.objects.all()
    
    if estado:
        vehiculos_qs = vehiculos_qs.filter(estado=estado)

    vehiculos_data = []
    for v in vehiculos_qs:
        vehiculos_data.append({
            'id': v.id,
            'placa': v.placa,
            'numero_serie': v.numero_serie, 
            'marca': v.marca,
            'modelo': v.modelo,
            'anio': v.anio,
            'tipo': v.get_tipo_display(),
            'kilometraje': round(v.kilometraje_actual, 2),
            'estado_display': ESTADOS.get(v.estado, 'Desconocido'),
            'estado_class': BADGE_CLASSES.get(v.estado, 'bg-danger'),
            'fecha_ultimo_mantenimiento': v.fecha_ultimo_mantenimiento,
        })

    # Paginación
    paginator = Paginator(vehiculos_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'vehiculos': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'estados_filtro': ESTADOS.items(),
        'estado_seleccionado': estado,
    }
    return render(request, 'flota/vehiculos/lista.html', context)

@login_required
@rol_requerido('administrador', 'supervisor')
def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario_registro = request.user
            vehiculo.save()
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm()
    
    return render(request, 'flota/vehiculos/registrar.html', {
        'form': form
    })

@login_required
def lista_mantenimientos(request):
    preventivos = MantenimientoPreventivo.objects.all()
    correctivos = MantenimientoCorrectivo.objects.all()
    return render(request, 'flota/mantenimientos/lista.html', {
        'preventivos': preventivos,
        'correctivos': correctivos
    })



@login_required
def lista_mantenimientos_preventivos(request):
    ESTADOS = {
        'pendiente': 'Pendiente',
        'completado': 'Completado',
        'cancelado': 'Cancelado',
    }

    BADGE_CLASSES = {
        'pendiente': 'bg-warning text-dark',
        'completado': 'bg-success',
        'cancelado': 'bg-danger'
    }
    estado = request.GET.get('estado')
    mantenimientos_qs = MantenimientoPreventivo.objects.select_related('vehiculo', 'usuario_registro').all().order_by('-fecha_registro')
    
    if estado:
        mantenimientos_qs = mantenimientos_qs.filter(estado=estado)

    mantenimientos_data = []
    for m in mantenimientos_qs:
        mantenimientos_data.append({
            'id': m.id,
            'vehiculo': str(m.vehiculo),
            'tipo': m.tipo,  # O usa m.get_tipo_display() si hay choices
            'estado_display': ESTADOS.get(m.estado, 'Desconocido'),
            'estado_class': BADGE_CLASSES.get(m.estado, 'bg-danger'),
            'fecha_prox_mantenimiento': m.fecha_prox_mantenimiento,
            'fecha_registro': m.fecha_registro,
            'usuario_registro': str(m.usuario_registro),
        })

    paginator = Paginator(mantenimientos_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'mantenimientos': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'estados_filtro': ESTADOS.items(),
        'estado_seleccionado': estado,
    }

    return render(request, 'flota/mantenimientos/preventivos/lista.html', context)

@login_required
@rol_requerido('administrador', 'supervisor')
def registrar_mantenimiento_preventivo(request):
    if request.method == 'POST':
        form = MantenimientoPreventivoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.usuario_registro = request.user
            mantenimiento.save()
            return redirect('lista_mantenimientos_preventivos')
    else:
        form = MantenimientoPreventivoForm()
    
    return render(request, 'flota/mantenimientos/preventivos/registrar.html', {
        'form': form,
        'titulo': 'Nuevo Mantenimiento Preventivo'
    })

@login_required
def detalle_mantenimiento_preventivo(request, pk):
    mantenimiento = get_object_or_404(MantenimientoPreventivo, pk=pk)
    
    context = {
        'mantenimiento': mantenimiento,
        'vehiculo': mantenimiento.vehiculo,
        'estado_display': mantenimiento.get_estado_display(),
        'usuario': mantenimiento.usuario_registro,
    }

    return render(request, 'flota/mantenimientos/preventivos/detalle.html', context)


@login_required
@rol_requerido('administrador')
def editar_mantenimiento_preventivo(request, pk):
    mantenimiento = get_object_or_404(MantenimientoPreventivo, pk=pk)
    if request.method == "POST":
        form = MantenimientoPreventivoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            return redirect('detalle_mantenimiento_preventivo', pk=mantenimiento.pk)
    else:
        form = MantenimientoPreventivoForm(instance=mantenimiento)
    
    return render(request, 'flota/mantenimientos/preventivos/editar.html', {
        'form': form,
        'mantenimiento': mantenimiento,
    })



@login_required
def lista_mantenimientos_correctivos(request):

    ESTADOS = {
        'reportado': 'Reportado',
        'en_proceso': 'En Proceso',
        'completado': 'Completado',
        'cancelado': 'Cancelado',
    }
    BADGE_CLASSES = {
        'reportado': 'bg-primary',
        'en_proceso': 'bg-warning text-dark',
        'completado': 'bg-success',
        'cancelado': 'bg-danger'
    }
    estado = request.GET.get('estado')
    mantenimientos_qs = MantenimientoCorrectivo.objects.select_related('vehiculo', 'usuario_registro').all().order_by('-fecha_reporte')
    
    if estado:
        mantenimientos_qs = mantenimientos_qs.filter(estado=estado)

    mantenimientos_data = []
    for m in mantenimientos_qs:
        mantenimientos_data.append({
            'id': m.id,
            'vehiculo': str(m.vehiculo),
            'prioridad': m.prioridad,
            'descripcion': m.descripcion_falla,
            'estado_display': ESTADOS.get(m.estado, 'Desconocido'),
            'estado_class': BADGE_CLASSES.get(m.estado, 'bg-danger'),
            'fecha_reporte': m.fecha_reporte,
            'fecha_ejecucion': m.fecha_solucion,
            'usuario_registro': str(m.usuario_registro),
        })

    paginator = Paginator(mantenimientos_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'mantenimientos': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'estados_filtro': ESTADOS.items(),
        'estado_seleccionado': estado,
    }

    return render(request, 'flota/mantenimientos/correctivos/lista.html', context)

@login_required
@rol_requerido('administrador', 'supervisor')
def registrar_mantenimiento_correctivo(request):
    if request.method == 'POST':
        form = MantenimientoCorrectivoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.usuario_registro = request.user
            mantenimiento.save()
            return redirect('lista_mantenimientos_correctivos')
    else:
        form = MantenimientoCorrectivoForm()
    
    return render(request, 'flota/mantenimientos/correctivos/registrar.html', {
        'form': form,
        'titulo': 'Nuevo Mantenimiento Correctivo'
    })

@login_required
def detalle_mantenimiento_correctivo(request, pk):
    mantenimiento = get_object_or_404(MantenimientoCorrectivo, pk=pk)
    
    context = {
        'mantenimiento': mantenimiento,
        'vehiculo': mantenimiento.vehiculo,
        'estado_display': mantenimiento.get_estado_display(),
        'prioridad_display': mantenimiento.get_prioridad_display(),
        'usuario': mantenimiento.usuario_registro,
    }

    return render(request, 'flota/mantenimientos/correctivos/detalle.html', context)


@login_required
@rol_requerido('administrador')
def editar_mantenimiento_correctivo(request, pk):
    mantenimiento = get_object_or_404(MantenimientoCorrectivo, pk=pk)
    if request.method == "POST":
        form = MantenimientoCorrectivoForm(request.POST, instance=mantenimiento)
        if form.is_valid():
            form.save()
            return redirect('detalle_mantenimiento_correctivo', pk=mantenimiento.pk)
    else:
        form = MantenimientoCorrectivoForm(instance=mantenimiento)
    
    return render(request, 'flota/mantenimientos/correctivos/editar.html', {
        'form': form,
        'mantenimiento': mantenimiento,
    })

@login_required
def calendario(request):
    # Parámetros de filtro
    tipo_filtro = request.GET.get('tipo', '')
    estado_filtro = request.GET.get('estado', '')
    
    # Consulta base para preventivos
    preventivos = MantenimientoPreventivo.objects.all().annotate(
        tipo_mantenimiento=F('tipo'),
        fecha=F('fecha_prox_mantenimiento'),
        tipo_categoria=Value('preventivo'),
        estado_mostrar=F('estado')  # Usamos el campo original
    ).values(
        'id', 'vehiculo__placa', 'tipo_mantenimiento', 'fecha', 
        'estado', 'descripcion', 'tipo_categoria', 'estado_mostrar'
    )
    
    # Consulta base para correctivos
    correctivos = MantenimientoCorrectivo.objects.all().annotate(
        tipo_mantenimiento=F('descripcion_falla'),
        fecha=F('fecha_solucion'),
        tipo_categoria=Value('correctivo'),
        estado_mostrar=F('estado')  # Usamos el campo original
    ).values(
        'id', 'vehiculo__placa', 'tipo_mantenimiento', 'fecha', 
        'estado', 'solucion_aplicada', 'tipo_categoria', 'estado_mostrar'
    )
    
    # Aplicar filtros
    if tipo_filtro:
        if tipo_filtro == 'preventivo':
            correctivos = correctivos.none()
        elif tipo_filtro == 'correctivo':
            preventivos = preventivos.none()
    
    if estado_filtro:
        preventivos = preventivos.filter(estado=estado_filtro)
        correctivos = correctivos.filter(estado=estado_filtro)
    
    # Combinar y ordenar por fecha ascendente (más cercana primero)
    mantenimientos = sorted(
        chain(preventivos, correctivos),
        key=lambda x: x['fecha'] if x['fecha'] else timezone.now().date()
    )
    
    # Paginación (15 items por página)
    paginator = Paginator(mantenimientos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estados disponibles para los filtros
    estados_preventivos = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ]
    
    estados_correctivos = [
        ('reportado', 'Reportado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    ]
    
    return render(request, 'flota/calendario.html', {
        'page_obj': page_obj,
        'hoy': timezone.now().date(),
        'tipo_seleccionado': tipo_filtro,
        'estado_seleccionado': estado_filtro,
        'estados_preventivos': estados_preventivos,
        'estados_correctivos': estados_correctivos
    })

@login_required
def alertas(request):
    hoy = date.today()
    alertas = []
    
    # Alertas de mantenimiento preventivo
    for mp in MantenimientoPreventivo.objects.filter(estado='pendiente'):
        if mp.fecha_prox_mantenimiento and (mp.fecha_prox_mantenimiento - hoy) <= timedelta(days=7):
            alertas.append({
                'titulo': f'Mantenimiento Preventivo: {mp.tipo}',
                'descripcion': f'Vence el {mp.fecha_prox_mantenimiento.strftime("%d/%m/%Y")}',
                'fecha': mp.fecha_prox_mantenimiento,
                'vehiculo': mp.vehiculo
            })
    
    return render(request, 'flota/alertas.html', {
        'alertas': alertas
    })