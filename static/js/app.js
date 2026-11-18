document.getElementById('churn-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    // 1. Recolectar y formatear los valores del formulario
    const datosCliente = {
        id_cliente: document.getElementById('id_cliente').value,
        edad: parseFloat(document.getElementById('edad').value),
        ingresos_anuales: parseFloat(document.getElementById('ingresos_anuales').value),
        saldo_cuenta: parseFloat(document.getElementById('saldo_cuenta').value),
        num_productos: parseInt(document.getElementById('num_productos').value),
        tiene_tarjeta: parseInt(document.getElementById('tiene_tarjeta').value),
        antiguedad_meses: parseInt(document.getElementById('antiguedad_meses').value),
        tipo_cuenta: document.getElementById('tipo_cuenta').value,
        canal_preferido: document.getElementById('canal_preferido').value,
        nivel_estudios: document.getElementById('nivel_estudios').value,
        nivel_satisfaccion: document.getElementById('nivel_satisfaccion').value
    };

    const btnSubmit = document.getElementById('btn-submit');
    btnSubmit.disabled = true;
    btnSubmit.textContent = 'Calculando predicción...';

    try {
        // 2. Petición POST al endpoint de FastAPI
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosCliente)
        });

        if (!response.ok) {
            throw new Error('Error en el servidor al procesar la inferencia.');
        }

        const resultado = await response.json();

        // 3. Renderizar los resultados en la interfaz
        document.getElementById('placeholder-result').classList.add('hidden');
        document.getElementById('result-content').classList.remove('hidden');

        document.getElementById('res-id').textContent = resultado.id_cliente;
        
        // Estado de abandono (0 o 1)
        const spanAbandono = document.getElementById('res-abandono');
        if (resultado.abandono === 1) {
            spanAbandono.textContent = 'Sí (Abandona)';
            spanAbandono.className = 'value badge badge-churn';
        } else {
            spanAbandono.textContent = 'No (Permanece)';
            spanAbandono.className = 'value badge badge-stay';
        }

        // Probabilidad de abandono en formato porcentaje
        document.getElementById('res-prob').textContent = (resultado.probabilidad_abandono * 100).toFixed(2) + ' %';

        // Nivel de riesgo con color dinámico
        const spanRiesgo = document.getElementById('res-riesgo');
        spanRiesgo.textContent = resultado.nivel_riesgo;
        spanRiesgo.className = 'value badge-risk risk-' + resultado.nivel_riesgo.toLowerCase();

        // Acción comercial recomendada
        document.getElementById('res-accion').textContent = resultado.accion_recomendada;

    } catch (error) {
        alert('Hubo un error al conectar con la API: ' + error.message);
    } finally {
        btnSubmit.disabled = false;
        btnSubmit.textContent = 'Evaluar Riesgo de Fuga';
    }
});