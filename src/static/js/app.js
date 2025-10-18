const API_URL = window.location.origin;

const elements = {
    form: document.getElementById('bfsForm'),
    selectOrigen: document.getElementById('origen'),
    selectDestino: document.getElementById('destino'),
    loading: document.getElementById('loading'),
    resultado: document.getElementById('resultado')
};

document.addEventListener('DOMContentLoaded', () => {
    cargarMunicipios();
    setupEventListeners();
});

function setupEventListeners() {
    elements.form.addEventListener('submit', handleSubmit);
}

async function cargarMunicipios() {
    try {
        const response = await fetch(`${API_URL}/api/municipios`);
        const data = await response.json();
        
        if (data.success && data.data) {
            poblarSelects(data.data);
        }
    } catch (error) {
        console.error('Error al cargar municipios:', error);
        mostrarError('Error al cargar los municipios. Intenta recargar la página.');
    }
}

async function buscarRuta(origen, destino) {
    try {
        const response = await fetch(`${API_URL}/api/buscar-ruta`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ origen, destino })
        });

        return await response.json();
    } catch (error) {
        throw new Error('Error de conexión con el servidor');
    }
}


async function handleSubmit(e) {
    e.preventDefault();
    
    const origen = elements.selectOrigen.value;
    const destino = elements.selectDestino.value;
    
    if (!validarFormulario(origen, destino)) {
        return;
    }

    mostrarLoading(true);
    ocultarResultado();

    try {
        const data = await buscarRuta(origen, destino);
        
        setTimeout(() => {
            mostrarLoading(false);
            
            if (data.success) {
                mostrarRutaExitosa(data);
            } else {
                mostrarError(data.error || 'No se encontró una ruta entre los municipios');
            }
        }, 800); 
        
    } catch (error) {
        mostrarLoading(false);
        mostrarError(error.message);
    }
}


function validarFormulario(origen, destino) {
    if (!origen || !destino) {
        mostrarError('Por favor selecciona origen y destino');
        return false;
    }
    
    if (origen === destino) {
        mostrarError('El origen y destino deben ser diferentes');
        return false;
    }
    
    return true;
}


function poblarSelects(municipios) {
    const opciones = municipios.map(m => 
        `<option value="${m}">${m}</option>`
    ).join('');
    
    elements.selectOrigen.innerHTML = '<option value="">Seleccionar municipio</option>' + opciones;
    elements.selectDestino.innerHTML = '<option value="">Seleccionar municipio</option>' + opciones;
}

function mostrarLoading(show) {
    if (show) {
        elements.loading.classList.add('active');
    } else {
        elements.loading.classList.remove('active');
    }
}

function ocultarResultado() {
    elements.resultado.classList.remove('active', 'success', 'error');
}

function mostrarRutaExitosa(data) {
    const rutaHTML = generarRutaHTML(data.ruta);
    const visitadosHTML = generarVisitadosHTML(data.visitados);
    
    elements.resultado.className = 'resultado success active';
    elements.resultado.innerHTML = `
        <div class="resultado-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
            </svg>
            <h3>Ruta Encontrada</h3>
        </div>
        
        <div class="info-card">
            <div class="info-label">Distancia Total</div>
            <div class="metric">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
                </svg>
                ${data.distancia} ${data.distancia === 1 ? 'conexión' : 'conexiones'}
            </div>
        </div>

        <div class="info-card">
            <div class="info-label">Recorrido Óptimo</div>
            <div class="ruta-visual">
                ${rutaHTML}
            </div>
        </div>

        <div class="info-card">
            <div class="info-label">Nodos Explorados (${data.visitados.length})</div>
            <div class="visitados-grid">
                ${visitadosHTML}
            </div>
        </div>
    `;
}

function mostrarError(mensaje) {
    elements.resultado.className = 'resultado error active';
    elements.resultado.innerHTML = `
        <div class="resultado-header">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="15" y1="9" x2="9" y2="15"/>
                <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
            <h3>Error</h3>
        </div>
        <div class="info-card">
            <p style="color: var(--text-secondary); margin: 0;">${mensaje}</p>
        </div>
    `;
}

function generarRutaHTML(ruta) {
    return ruta.map((nodo, index) => {
        const esUltimo = index === ruta.length - 1;
        return `
            <span class="nodo">${nodo}</span>
            ${!esUltimo ? '<span class="flecha">→</span>' : ''}
        `;
    }).join('');
}

function generarVisitadosHTML(visitados) {
    return visitados.map(nodo => 
        `<span class="visitado">${nodo}</span>`
    ).join('');
}

function animateElement(element, animation) {
    element.style.animation = 'none';
    setTimeout(() => {
        element.style.animation = animation;
    }, 10);
}