const API_URL = 'http://localhost:8080';
let token = localStorage.getItem('token');

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        showApp();
    }
    
    // Auth Listeners
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    // Navigation Listeners
    document.querySelectorAll('.nav-link[data-view]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchView(link.getAttribute('data-view'));
        });
    });
});

// --- Auth ---
async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);
    
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            token = data.access_token;
            localStorage.setItem('token', token);
            showApp();
        } else {
            document.getElementById('login-error').classList.remove('hidden');
        }
    } catch (err) {
        showToast('Error de conexión con el servidor');
    }
}

function handleLogout() {
    token = null;
    localStorage.removeItem('token');
    document.getElementById('app-layout').classList.add('hidden');
    document.getElementById('login-overlay').classList.remove('hidden');
}

function showApp() {
    document.getElementById('login-overlay').classList.add('hidden');
    document.getElementById('app-layout').classList.remove('hidden');
    switchView('dashboard');
}

// --- Navigation ---
function switchView(view) {
    // Update menu state
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelector(`.nav-link[data-view="${view}"]`)?.classList.add('active');
    
    // Update title
    const titles = {
        dashboard: 'Dashboard',
        clientes: 'Gestión de Clientes',
        mascotas: 'Gestión de Mascotas',
        consultas: 'Citas Médicas',
        facturacion: 'Facturación'
    };
    document.getElementById('view-title').textContent = titles[view] || 'Sistema';
    
    // Load View Data
    loadViewData(view);
}

async function loadViewData(view) {
    const container = document.getElementById('view-container');
    container.innerHTML = '<div class="text-center p-5"><div class="spinner-border text-primary" role="status"></div></div>';
    
    try {
        switch (view) {
            case 'dashboard':
                await renderDashboard();
                break;
            case 'clientes':
                await renderClientes();
                break;
            case 'mascotas':
                await renderMascotas();
                break;
            case 'consultas':
                await renderConsultas();
                break;
            case 'facturacion':
                await renderFacturacion();
                break;
            default:
                container.innerHTML = `<h3>Sección: ${view}</h3><p>Próximamente...</p>`;
        }
    } catch (err) {
        console.error(err);
        container.innerHTML = '<div class="alert alert-danger">Error al cargar datos. Asegúrate que el backend esté corriendo.</div>';
    }
}

// --- Modals ---
let clienteModal, mascotaModal;

function showClienteModal() {
    if (!clienteModal) clienteModal = new bootstrap.Modal(document.getElementById('cliente-modal'));
    document.getElementById('cliente-form').reset();
    clienteModal.show();
}

async function saveCliente() {
    const data = {
        nombre: document.getElementById('cli-nombre').value,
        documento: document.getElementById('cli-documento').value,
        telefono: document.getElementById('cli-telefono').value,
        email: document.getElementById('cli-email').value,
        direccion: document.getElementById('cli-direccion').value
    };

    try {
        await apiFetch('/personas/clientes', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        clienteModal.hide();
        showToast('Cliente guardado con éxito');
        renderClientes();
    } catch (err) {
        showToast('Error al guardar cliente');
    }
}

async function showMascotaModal(defaultClienteId = null) {
    if (!mascotaModal) mascotaModal = new bootstrap.Modal(document.getElementById('mascota-modal'));
    document.getElementById('mascota-form').reset();
    
    // Load clients for the dropdown
    const clientes = await apiFetch('/personas/clientes');
    const select = document.getElementById('mas-cliente');
    select.innerHTML = '<option value="">Sin dueño (Agregación)</option>';
    
    clientes.forEach(c => {
        const selected = (defaultClienteId == c.id_cliente) ? 'selected' : '';
        select.innerHTML += `<option value="${c.id_cliente}" ${selected}>${c.nombre}</option>`;
    });
    
    mascotaModal.show();
}

async function saveMascota() {
    const clienteId = document.getElementById('mas-cliente').value;
    const data = {
        nombre: document.getElementById('mas-nombre').value,
        especie: document.getElementById('mas-especie').value,
        raza: document.getElementById('mas-raza').value,
        fecha_nacimiento: document.getElementById('mas-fecha').value || null,
        id_cliente: clienteId ? parseInt(clienteId) : null
    };

    try {
        await apiFetch('/mascotas/', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        mascotaModal.hide();
        showToast('Mascota guardada con éxito');
        renderMascotas();
    } catch (err) {
        showToast('Error al guardar mascota');
    }
}

// --- Views Rendering ---

async function renderDashboard() {
    const stats = await apiFetch('/personas/clientes'); // Simple example
    const mascotas = await apiFetch('/mascotas/');
    
    document.getElementById('view-container').innerHTML = `
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card p-4">
                    <h6 class="text-muted">Clientes Totales</h6>
                    <h2>${stats.length}</h2>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-4">
                    <h6 class="text-muted">Mascotas en Lista</h6>
                    <h2>${mascotas.length}</h2>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card p-4 bg-primary text-white">
                    <h6>Acceso Rápido</h6>
                    <button class="btn btn-light btn-sm mt-2" onclick="switchView('clientes')">Nuevo Cliente</button>
                </div>
            </div>
        </div>
    `;
}

async function renderClientes() {
    const clientes = await apiFetch('/personas/clientes');
    
    let html = `
        <div class="d-flex justify-content-between mb-4">
            <h4>Clientes Registrados</h4>
            <button class="btn btn-primary" onclick="showClienteModal()">+ Nuevo Cliente</button>
        </div>
        <div class="card">
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Documento</th>
                            <th>Teléfono</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    clientes.forEach(c => {
        html += `
            <tr>
                <td>${c.nombre}</td>
                <td>${c.documento}</td>
                <td>${c.telefono || '-'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="viewMascotas(${c.id_cliente})">Ver Mascotas</button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div></div>';
    document.getElementById('view-container').innerHTML = html;
}

async function renderMascotas(filterClienteId = null) {
    const mascotas = await apiFetch('/mascotas/');
    const filtered = filterClienteId ? mascotas.filter(m => m.id_cliente == filterClienteId) : mascotas;

    let html = `
        <div class="d-flex justify-content-between mb-4">
            <h4>Mascotas Registradas ${filterClienteId ? '(Filtrado)' : ''}</h4>
            <button class="btn btn-primary" onclick="showMascotaModal(${filterClienteId})">+ Nueva Mascota</button>
        </div>
        <div class="row g-3">
    `;

    if (filtered.length === 0) {
        html += '<div class="col-12 text-center p-5 text-muted">No se encontraron mascotas.</div>';
    }

    filtered.forEach(m => {
        html += `
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title"><i class="bi bi-paw me-2"></i>${m.nombre}</h5>
                        <p class="card-text mb-1 text-muted">${m.especie} - ${m.raza || 'Mestizo'}</p>
                        <p class="small text-muted">Nacimiento: ${m.fecha_nacimiento || 'Desconocido'}</p>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    document.getElementById('view-container').innerHTML = html;
}

function viewMascotas(clienteId) {
    switchView('mascotas');
    setTimeout(() => renderMascotas(clienteId), 100); // Slight delay to ensure switchView is done
}

async function renderConsultas() {
    // Basic table view for now
    document.getElementById('view-container').innerHTML = `
        <div class="d-flex justify-content-between mb-4">
            <h4>Citas y Consultas</h4>
            <button class="btn btn-primary" disabled>+ Nueva Cita (Próximamente)</button>
        </div>
        <div class="alert alert-info">Esta sección está lista para integrar con el módulo de Citas.</div>
    `;
}

async function renderFacturacion() {
    document.getElementById('view-container').innerHTML = `
        <div class="d-flex justify-content-between mb-4">
            <h4>Control de Facturación</h4>
            <button class="btn btn-primary" disabled>+ Nueva Factura (Próximamente)</button>
        </div>
        <div class="alert alert-info">Cargando historial de facturas...</div>
    `;
}

// --- Utils ---

async function apiFetch(endpoint, options = {}) {
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
    if (response.status === 401) handleLogout();
    if (!response.ok) throw new Error('API Error');
    return response.json();
}

function showToast(msg) {
    document.getElementById('toast-message').textContent = msg;
    const toast = new bootstrap.Toast(document.getElementById('liveToast'));
    toast.show();
}
