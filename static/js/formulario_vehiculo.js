document.addEventListener('DOMContentLoaded', function () {
    const selectVehiculo = document.getElementById('id_vehiculo');
    const kmProximoInput = document.getElementById('id_km_prox_mantenimiento');
    const infoVehiculo = document.getElementById('info-vehiculo');

    let kilometrajeActual = null;

    function cargarDatosVehiculo(vehiculoId) {
        if (!vehiculoId) {
            infoVehiculo.innerHTML = '';
            kilometrajeActual = null;
            if (kmProximoInput) kmProximoInput.removeAttribute('min');
            return;
        }

        fetch(`/vehiculos/datos/?vehiculo_id=${vehiculoId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    infoVehiculo.innerHTML = '';
                    kilometrajeActual = null;
                    if (kmProximoInput) kmProximoInput.removeAttribute('min');
                    return;
                }

                kilometrajeActual = parseInt(data.kilometraje_actual);

                if (kmProximoInput) {
                    kmProximoInput.setAttribute('min', kilometrajeActual + 1);
                }

                infoVehiculo.innerHTML = `
                    <div class="card mt-3 border-info">
                        <div class="card-body p-3">
                            <h5 class="card-title text-info mb-3">
                                <i class="bi bi-info-circle me-2"></i> Datos del Vehículo Seleccionado
                            </h5>
                            <div class="row g-2">
                                <div class="col-md-3"><strong>Marca:</strong> ${data.marca}</div>
                                <div class="col-md-3"><strong>Modelo:</strong> ${data.modelo}</div>
                                <div class="col-md-2"><strong>Año:</strong> ${data.anio}</div>
                                <div class="col-md-4"><strong>Kilometraje Actual:</strong> 
                                    <span id="km-actual">${data.kilometraje_actual}</span> km
                                </div>
                                <div class="col-md-4"><strong>Fecha Último Mantenimiento:</strong> ${data.fecha_ultimo_mantenimiento || 'N/A'}</div>
                                <div class="col-md-4"><strong>Tipo:</strong> ${data.tipo}</div>
                                <div class="col-md-4"><strong>Estado:</strong> ${data.estado}</div>
                                <div class="col-md-4"><strong>Número de Serie:</strong> ${data.numero_serie}</div>
                            </div>
                        </div>
                    </div>
                `;
            })
            .catch(error => {
                console.error('Error al obtener datos del vehículo:', error);
                infoVehiculo.innerHTML = '';
                kilometrajeActual = null;
                if (kmProximoInput) kmProximoInput.removeAttribute('min');
            });
    }

    selectVehiculo.addEventListener('change', function () {
        cargarDatosVehiculo(this.value);
    });

    if (kmProximoInput) {
        kmProximoInput.addEventListener('input', function () {
            const valor = parseInt(this.value);
            if (kilometrajeActual !== null && valor <= kilometrajeActual) {
                this.setCustomValidity('Debe ser mayor que el kilometraje actual del vehículo.');
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Al cargar la página, si ya hay un vehículo seleccionado, cargar los datos
    if (selectVehiculo.value) {
        cargarDatosVehiculo(selectVehiculo.value);
    }
});
